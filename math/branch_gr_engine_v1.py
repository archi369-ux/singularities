
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union
import math


@dataclass(frozen=True)
class Guard:
    atoms: Tuple[Tuple[str, str, float], ...] = field(default_factory=tuple)

    def __and__(self, other: "Guard") -> Optional["Guard"]:
        merged = list(self.atoms) + list(other.atoms)
        normalized: Dict[str, Dict[str, float]] = {}
        for var, op, val in merged:
            if var not in normalized:
                normalized[var] = {}
            normalized[var][op] = val
        for var, ops in normalized.items():
            if "==" in ops and "!=" in ops and ops["=="] == ops["!="]:
                return None
        canonical = []
        seen = set()
        for atom in merged:
            if atom not in seen:
                seen.add(atom)
                canonical.append(atom)
        canonical.sort()
        return Guard(tuple(canonical))

    def is_true_for(self, values: Dict[str, float], tol: float = 1e-12) -> bool:
        for var, op, val in self.atoms:
            if var not in values:
                return False
            x = values[var]
            if op == "==":
                if not math.isclose(x, val, abs_tol=tol):
                    return False
            elif op == "!=":
                if math.isclose(x, val, abs_tol=tol):
                    return False
            else:
                raise ValueError(f"Unsupported operator: {op}")
        return True

    def __str__(self) -> str:
        if not self.atoms:
            return "TRUE"
        return " ∧ ".join(f"{var} {op} {val:g}" for var, op, val in self.atoms)


TRUE_GUARD = Guard(())


def eq_guard(var: str, value: float = 0.0) -> Guard:
    return Guard(((var, "==", value),))


def neq_guard(var: str, value: float = 0.0) -> Guard:
    return Guard(((var, "!=", value),))


@dataclass(frozen=True)
class CoreValue:
    name: str
    metadata: Dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
        if self.metadata:
            meta = ", ".join(f"{k}={v}" for k, v in self.metadata.items())
            return f"{self.name}<{meta}>"
        return self.name


ScalarValue = Union[float, CoreValue]


@dataclass
class Branch:
    cases: List[Tuple[Guard, ScalarValue]]

    def simplify(self) -> "Branch":
        self.cases = [(g, v) for g, v in self.cases if g is not None]
        return self

    def map_values(self, fn: Callable[[ScalarValue], ScalarValue]) -> "Branch":
        return Branch([(g, fn(v)) for g, v in self.cases]).simplify()

    def combine(self, other: "Branch", op: Callable[[ScalarValue, ScalarValue], ScalarValue]) -> "Branch":
        new_cases: List[Tuple[Guard, ScalarValue]] = []
        for g1, v1 in self.cases:
            for g2, v2 in other.cases:
                g = g1 & g2
                if g is not None:
                    new_cases.append((g, op(v1, v2)))
        return Branch(new_cases).simplify()

    def evaluate(self, values: Dict[str, float]) -> ScalarValue:
        matches = [(g, v) for g, v in self.cases if g.is_true_for(values)]
        if not matches:
            raise ValueError(f"No branch matched values={values}")
        if len(matches) > 1:
            raise ValueError(f"Ambiguous branch match for values={values}: {matches}")
        return matches[0][1]

    def pretty(self) -> str:
        lines = ["Branch{"]
        for g, v in self.cases:
            lines.append(f"  [{g}] -> {v}")
        lines.append("}")
        return "\n".join(lines)


def _binary_numeric_or_core(
    a: ScalarValue,
    b: ScalarValue,
    numeric_op: Callable[[float, float], float],
    opname: str,
) -> ScalarValue:
    if isinstance(a, CoreValue) or isinstance(b, CoreValue):
        return CoreValue(f"{opname}({a},{b})")
    return numeric_op(float(a), float(b))


def branch_add(a: Branch, b: Branch) -> Branch:
    return a.combine(b, lambda x, y: _binary_numeric_or_core(x, y, lambda p, q: p + q, "ADD"))


def branch_mul(a: Branch, b: Branch) -> Branch:
    return a.combine(b, lambda x, y: _binary_numeric_or_core(x, y, lambda p, q: p * q, "MUL"))


def branch_neg(a: Branch) -> Branch:
    return a.map_values(lambda x: CoreValue(f"NEG({x})") if isinstance(x, CoreValue) else -float(x))


def branch_sub(a: Branch, b: Branch) -> Branch:
    return branch_add(a, branch_neg(b))


def branch_pow(a: Branch, n: int) -> Branch:
    if not isinstance(n, int):
        raise ValueError("v1 only supports integer powers")
    def op(x: ScalarValue) -> ScalarValue:
        if isinstance(x, CoreValue):
            return CoreValue(f"POW({x},{n})")
        return float(x) ** n
    return a.map_values(op)


def const_branch(x: float) -> Branch:
    return Branch([(TRUE_GUARD, float(x))])


class Expr:
    def eval_branch(self) -> Branch:
        raise NotImplementedError

    def zero_sets(self) -> List[str]:
        return []


@dataclass(frozen=True)
class Const(Expr):
    value: float

    def eval_branch(self) -> Branch:
        return const_branch(self.value)

    def __str__(self) -> str:
        return f"{self.value:g}"


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def eval_branch(self) -> Branch:
        raise ValueError(f"Raw variable '{self.name}' cannot evaluate to a branch by itself in this prototype.")

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr

    def eval_branch(self) -> Branch:
        return branch_add(self.left.eval_branch(), self.right.eval_branch())

    def zero_sets(self) -> List[str]:
        return self.left.zero_sets() + self.right.zero_sets()

    def __str__(self) -> str:
        return f"({self.left} + {self.right})"


@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr

    def eval_branch(self) -> Branch:
        return branch_mul(self.left.eval_branch(), self.right.eval_branch())

    def zero_sets(self) -> List[str]:
        return self.left.zero_sets() + self.right.zero_sets()

    def __str__(self) -> str:
        return f"({self.left} * {self.right})"


@dataclass(frozen=True)
class Pow(Expr):
    base: Expr
    exponent: int

    def eval_branch(self) -> Branch:
        return branch_pow(self.base.eval_branch(), self.exponent)

    def zero_sets(self) -> List[str]:
        return self.base.zero_sets()

    def __str__(self) -> str:
        return f"({self.base}^{self.exponent})"


@dataclass(frozen=True)
class Quot(Expr):
    numerator: Expr
    denominator: Expr
    core_name: str = "CORE"

    def _denominator_zero_var(self) -> str:
        d = self.denominator
        if isinstance(d, Var):
            return d.name
        if isinstance(d, Pow) and isinstance(d.base, Var) and isinstance(d.exponent, int) and d.exponent > 0:
            return d.base.name
        raise ValueError("v1 zero-set detector only supports denominator Var(x) or Pow(Var(x), positive_int)")

    def eval_branch(self) -> Branch:
        var = self._denominator_zero_var()
        num = self.numerator
        den = self.denominator
        num_branch = num.eval_branch()

        if isinstance(num, Const) and isinstance(den, Var):
            nonzero_val: ScalarValue = CoreValue("EXPR", {"form": f"{num.value:g}/{den.name}", "guard": f"{den.name}!=0"})
        elif isinstance(num, Const) and isinstance(den, Pow) and isinstance(den.base, Var):
            nonzero_val = CoreValue("EXPR", {"form": f"{num.value:g}/{den.base.name}^{den.exponent}", "guard": f"{den.base.name}!=0"})
        else:
            nonzero_val = CoreValue("EXPR", {"form": f"({num})/({den})", "guard": f"{var}!=0"})

        zero_cases: List[Tuple[Guard, ScalarValue]] = []
        for g, v in num_branch.cases:
            gz = g & eq_guard(var, 0.0)
            if gz is not None:
                zero_cases.append((gz, CoreValue(self.core_name, {"denominator_zero": var, "numerator": str(v)})))

        nonzero_cases = [(neq_guard(var, 0.0), nonzero_val)]
        return Branch(nonzero_cases + zero_cases).simplify()

    def zero_sets(self) -> List[str]:
        return [self._denominator_zero_var()] + self.numerator.zero_sets()

    def __str__(self) -> str:
        return f"Quot({self.numerator}, {self.denominator})"


def substitute_numeric(expr: Expr, values: Dict[str, float]) -> float:
    if isinstance(expr, Const):
        return expr.value
    if isinstance(expr, Var):
        return float(values[expr.name])
    if isinstance(expr, Add):
        return substitute_numeric(expr.left, values) + substitute_numeric(expr.right, values)
    if isinstance(expr, Mul):
        return substitute_numeric(expr.left, values) * substitute_numeric(expr.right, values)
    if isinstance(expr, Pow):
        return substitute_numeric(expr.base, values) ** expr.exponent
    if isinstance(expr, Quot):
        num = substitute_numeric(expr.numerator, values)
        den = substitute_numeric(expr.denominator, values)
        return num / den
    raise TypeError(expr)


def detect_zero_sets(expr: Expr) -> List[str]:
    seen = []
    for v in expr.zero_sets():
        if v not in seen:
            seen.append(v)
    return seen


def schwarzschild_kretschmann_expr(A: float = 48.0) -> Expr:
    return Quot(Const(A), Pow(Var("r"), 6), core_name="C_K")


@dataclass
class RadialState:
    tau: float
    r: float
    v: float

    def __str__(self) -> str:
        return f"(tau={self.tau:.6f}, r={self.r:.6f}, v={self.v:.6f})"


@dataclass
class InfallResult:
    history: List[RadialState]
    outcome: str
    message: str

    def summary(self) -> str:
        lines = [f"Outcome: {self.outcome}", self.message, "Last states:"]
        tail = self.history[-5:] if len(self.history) >= 5 else self.history
        for s in tail:
            lines.append(f"  {s}")
        return "\n".join(lines)


def simulate_radial_infall(
    r0: float,
    M: float,
    dtau: float = 1e-3,
    max_steps: int = 2_000_000,
    policy: str = "terminate",
    core_reentry_radius: float = 1e-3,
) -> InfallResult:
    if r0 <= 0:
        raise ValueError("r0 must be > 0")
    if M <= 0:
        raise ValueError("M must be > 0")

    tau = 0.0
    r = float(r0)
    v = 0.0
    history: List[RadialState] = [RadialState(tau, r, v)]

    for _ in range(max_steps):
        if r <= 0.0:
            if policy == "terminate":
                return InfallResult(
                    history=history,
                    outcome="branch-boundary-termination",
                    message="Reached r <= 0. Classical evolution stopped at the core branch boundary.",
                )
            elif policy == "transition":
                r = core_reentry_radius
                v = abs(v)
                history.append(RadialState(tau, r, v))
                return InfallResult(
                    history=history,
                    outcome="branch-transition",
                    message="Reached r <= 0, then applied toy transition rule: re-entered at positive radius with outward velocity.",
                )
            else:
                raise ValueError("Unknown policy")

        a = -M / (r * r)
        v = v + a * dtau
        r = r + v * dtau
        tau = tau + dtau
        history.append(RadialState(tau, r, v))

    return InfallResult(
        history=history,
        outcome="max-steps",
        message="Simulation stopped before reaching branch boundary.",
    )


def demo_report() -> str:
    lines: List[str] = []
    lines.append("=== branch_gr_engine_v1 demo ===")
    lines.append("")
    expr = schwarzschild_kretschmann_expr(A=48.0)
    lines.append("1) Toy Schwarzschild scalar")
    lines.append(f"Expression: {expr}")
    lines.append(f"Detected zero sets: {detect_zero_sets(expr)}")
    lines.append("")
    lines.append("Branch lift:")
    lines.append(expr.eval_branch().pretty())
    lines.append("")
    lines.append("Classical numeric samples:")
    for r in [2.0, 1.0, 0.5, 0.1]:
        lines.append(f"r={r:g}: {substitute_numeric(expr, {'r': r})}")
    try:
        substitute_numeric(expr, {"r": 0.0})
    except ZeroDivisionError:
        lines.append("r=0: ZeroDivisionError (classical)")
    lines.append("")
    result_t = simulate_radial_infall(r0=1.0, M=0.1, dtau=1e-4, policy="terminate")
    lines.append("2) Reduced radial infall [termination]")
    lines.append(result_t.summary())
    lines.append("")
    result_x = simulate_radial_infall(r0=1.0, M=0.1, dtau=1e-4, policy="transition", core_reentry_radius=0.01)
    lines.append("3) Reduced radial infall [transition]")
    lines.append(result_x.summary())
    lines.append("")
    lines.append("Notes:")
    lines.append("- Exterior behavior is classical until r approaches 0.")
    lines.append("- Exact zero-hit is represented by a guarded core object.")
    lines.append("- Infall model is reduced, not full Schwarzschild GR.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(demo_report())
