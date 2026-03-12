# Results 1 HO Small-vs-Large Timestep Summary

Generated: 2026-03-12T20:27:33Z

| Integrator | dt | abs(x(T)-x_exact(T)) | abs(v(T)-v_exact(T)) | RMS phase-space error | max abs(E-E0)/abs(E0) |
|---|---|---|---|---|---|
| Forward Euler | 0.5 | 8.367e+00 | 1.953e+00 | 3.863e+00 | 8.574e+01 |
| Forward Euler | 0.01 | 4.321e-02 | 2.760e-02 | 2.942e-02 | 1.052e-01 |
| Velocity-Verlet | 0.5 | 6.303e-02 | 6.663e-02 | 6.544e-02 | 6.231e-02 |
| Velocity-Verlet | 0.01 | 2.267e-05 | 2.816e-05 | 2.574e-05 | 2.500e-05 |
| RK4 | 0.5 | 8.076e-04 | 5.127e-03 | 3.035e-03 | 4.196e-03 |
| RK4 | 0.01 | 4.475e-10 | 7.030e-10 | 4.812e-10 | 1.389e-11 |
