# Results 1 Figure Caption Notes (Auto-Generated)

Generated: 2026-03-10T22:50:07Z

Figure 1 (trajectories): Verifies x(t) and v(t) behaviour for all three methods against the exact solution at dt=0.01; Euler remains the visibly largest deviation while RK4 is nearly exact on this horizon.
Figure 2 (phase space): Shows geometric orbit quality at dt=0.01, with Euler clearly outside the closed exact orbit and a dedicated final-sector zoom showing all methods with endpoint markers.
Figure 3 (small vs large dt): Directly demonstrates timestep sensitivity with dt=0.5 and dt=0.01 for each method, retaining full coarse-range behaviour without dense in-panel text; quantitative values are provided in the summary tables; Forward Euler coarse/fine endpoint x-error ratio = 193.64; Velocity-Verlet coarse/fine endpoint x-error ratio = 2780.53; RK4 coarse/fine endpoint x-error ratio = 1804613.76.
Figure 4 (combined convergence): Fitted slopes are Euler 1.05/1.03, Velocity-Verlet 2.00/2.00, RK4 3.94/4.00 (endpoint/RMS), consistent with orders 1/2/4; filled markers denote fit-included points and open markers denote coarse points shown for context.
Figure 5 (energy diagnostic): At dt=0.01, Euler exhibits strong secular drift, Velocity-Verlet shows bounded oscillatory error, and RK4 drift is tiny on this interval; RK4 remains non-symplectic.
Figure 6 (error-vs-time diagnostic): At dt=0.1, Euler error grows monotonically, Velocity-Verlet error oscillates with bounded envelope (symplectic behaviour), and RK4 remains smallest on this horizon.
