# Results 1 Figure Caption Notes (Auto-Generated)

Generated: 2026-03-12T18:17:51Z

Figure 1(a-c) (combined diagnostics): Verifies x(t), v(t), and phase-space behaviour for all three methods against the exact solution at dt=0.01 in one shared-legend figure; Euler remains the visibly largest deviation while Velocity-Verlet and RK4 remain close to the exact orbit.
Figure 2(a-f) (small vs large dt): Compares coarse and fine timesteps (dt=0.5 and dt=0.01) for each method using time traces and phase portraits, while retaining the full coarse-range behaviour; quantitative values are provided in the summary tables; Forward Euler coarse/fine endpoint x-error ratio = 193.64; Velocity-Verlet coarse/fine endpoint x-error ratio = 2780.53; RK4 coarse/fine endpoint x-error ratio = 1804613.76.
Figure 3(a,b) (combined convergence): Measured orders are Euler 1.05/1.03, Velocity-Verlet 2.00/2.00, and RK4 3.94/4.00 (endpoint/RMS), consistent with 1/2/4; filled markers denote fit points and open markers show coarse-step context.
Figure 4(a) (energy diagnostic): At dt=0.01, Euler exhibits strong secular drift, Velocity-Verlet shows bounded oscillatory error, and RK4 drift is tiny on this interval; RK4 remains non-symplectic.
