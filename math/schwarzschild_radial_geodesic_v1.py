
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


@dataclass
class GeodesicState:
    tau: float
    r: float
    t: float | None
    dr_dtau: float
    dt_dtau: float | None
    kretschmann: float | str

    def line(self) -> str:
        t_str = "∞/undef" if self.t is None else f"{self.t:.6f}"
        dtdtau_str = "∞/undef" if self.dt_dtau is None else f"{self.dt_dtau:.6f}"
        k_str = self.kretschmann if isinstance(self.kretschmann, str) else f"{self.kretschmann:.6f}"
        return (
            f"tau={self.tau:.6f}, r={self.r:.6f}, t={t_str}, "
            f"dr/dtau={self.dr_dtau:.6f}, dt/dtau={dtdtau_str}, K={k_str}"
        )


@dataclass
class RunResult:
    history: list[GeodesicState]
    events: list[str]
    outcome: str

    def summary(self, tail: int = 8) -> str:
        lines = [f"Outcome: {self.outcome}", "Events:"]
        if self.events:
            lines.extend(f"- {e}" for e in self.events)
        else:
            lines.append("- none")
        lines.append("")
        lines.append("Last states:")
        for s in self.history[-tail:]:
            lines.append(s.line())
        return "\n".join(lines)


def kretschmann_scalar(M: float, r: float) -> float | str:
    if r == 0.0:
        return "C_K(core-branch)"
    return 48.0 * (M ** 2) / (r ** 6)


def radial_timelike_step(M: float, E: float, r: float) -> tuple[float, float | None]:
    """
    Schwarzschild radial timelike geodesic, L = 0, in geometric units G = c = 1.

    Equations:
        (dr/dtau)^2 = E^2 - (1 - 2M/r)
        dt/dtau     = E / (1 - 2M/r)

    For infall we choose the negative square root.
    """
    if r <= 0.0:
        return 0.0, None

    radicand = E * E - (1.0 - 2.0 * M / r)
    if radicand < 0 and abs(radicand) < 1e-12:
        radicand = 0.0
    if radicand < 0:
        raise ValueError(f"Radicand became negative: {radicand} at r={r}")

    dr_dtau = -sqrt(radicand)

    denom = 1.0 - 2.0 * M / r
    if abs(denom) < 1e-12:
        dt_dtau = None
    else:
        dt_dtau = E / denom

    return dr_dtau, dt_dtau


def simulate_schwarzschild_radial_geodesic(
    M: float = 1.0,
    E: float = 1.0,
    r0: float = 10.0,
    dtau: float = 1e-3,
    max_steps: int = 2_000_000,
    core_policy: str = "terminate",
    reentry_radius: float = 1e-2,
) -> RunResult:
    """
    Proper Schwarzschild radial timelike geodesic toy.

    What is proper here:
    - uses Schwarzschild radial geodesic first integrals
    - tracks coordinate time divergence at the horizon
    - tracks finite proper-time evolution inward

    What remains a toy:
    - no Kruskal/Eddington-Finkelstein coordinates
    - no tensor engine here
    - core transition is an imposed branch rule, not derived GR
    """
    if M <= 0:
        raise ValueError("M must be > 0")
    if E <= 0:
        raise ValueError("E must be > 0")
    if r0 <= 2.0 * M:
        raise ValueError("r0 should start outside the horizon for this demo")

    tau = 0.0
    r = r0
    t = 0.0
    crossed_horizon = False
    events: list[str] = []
    history: list[GeodesicState] = []

    for _ in range(max_steps):
        K = kretschmann_scalar(M, r)
        dr_dtau, dt_dtau = radial_timelike_step(M, E, r)

        history.append(
            GeodesicState(
                tau=tau,
                r=r,
                t=t,
                dr_dtau=dr_dtau,
                dt_dtau=dt_dtau,
                kretschmann=K,
            )
        )

        if not crossed_horizon and r <= 2.0 * M:
            crossed_horizon = True
            events.append(
                "Crossed r = 2M. Horizon encountered. This is treated as a coordinate issue for t, not a core branch."
            )

        if r <= 0.0:
            if core_policy == "terminate":
                events.append("Reached r = 0. Activated core branch boundary. Classical geodesic terminated.")
                return RunResult(history=history, events=events, outcome="core-termination")
            elif core_policy == "transition":
                events.append(
                    "Reached r = 0. Activated core branch boundary. Applied toy re-entry rule with outgoing branch."
                )
                history.append(
                    GeodesicState(
                        tau=tau,
                        r=reentry_radius,
                        t=None,
                        dr_dtau=abs(dr_dtau),
                        dt_dtau=None,
                        kretschmann=kretschmann_scalar(M, reentry_radius),
                    )
                )
                return RunResult(history=history, events=events, outcome="core-transition")
            else:
                raise ValueError("Unknown core_policy")

        # advance
        r_next = r + dr_dtau * dtau
        tau_next = tau + dtau

        if dt_dtau is None or not isfinite(dt_dtau):
            t_next = None
        else:
            if t is None:
                t_next = None
            else:
                t_next = t + dt_dtau * dtau

        # clamp tiny negative overshoot into exact zero for branch hit
        if r_next < 0.0 and abs(r_next) < 1e-8:
            r_next = 0.0

        r, tau, t = r_next, tau_next, t_next

    events.append("Stopped at max_steps before core branch was reached.")
    return RunResult(history=history, events=events, outcome="max-steps")


def demo_report() -> str:
    lines: list[str] = []
    lines.append("=== Schwarzschild radial geodesic v1 ===")
    lines.append("")
    lines.append("Units: G = c = 1")
    lines.append("Equations:")
    lines.append("  (dr/dtau)^2 = E^2 - (1 - 2M/r)")
    lines.append("  dt/dtau     = E / (1 - 2M/r)")
    lines.append("")
    lines.append("Interpretation:")
    lines.append("- horizon r=2M affects Schwarzschild coordinate time t")
    lines.append("- singular core r=0 is treated as the branch boundary")
    lines.append("")

    terminate = simulate_schwarzschild_radial_geodesic(
        M=1.0, E=1.0, r0=10.0, dtau=1e-3, core_policy="terminate"
    )
    lines.append("[Termination policy]")
    lines.append(terminate.summary())
    lines.append("")

    transition = simulate_schwarzschild_radial_geodesic(
        M=1.0, E=1.0, r0=10.0, dtau=1e-3, core_policy="transition", reentry_radius=0.05
    )
    lines.append("[Transition policy]")
    lines.append(transition.summary())
    lines.append("")

    lines.append("Notes:")
    lines.append("- Proper time stays finite on the way inward.")
    lines.append("- Schwarzschild coordinate time becomes ill-behaved at the horizon in this chart.")
    lines.append("- Kretschmann scalar grows like 48 M^2 / r^6 and is replaced by a core tag at r=0.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(demo_report())
