# Qu-Mudawar 2002: Fluent reconstruction results

Geometry was created in SolidWorks. A scripted conformal hex mesh was generated from the same rectilinear dimensions, independently checked against the STEP export, and solved in ANSYS Fluent 2024 R1.

All 13 cases passed numerical convergence checks. This is a reconstructed benchmark, not an exact validation: sensor differences reach 9.16 C versus digitized experiments and 4.04 C versus published numerical curves. The atmospheric high-heat, low-flow case exceeds local saturation; the separate 200 kPa pressure assumption passes the saturation checks below.

## Completed runs

| Case | Re | Heat flux (W/cm2) | Cells | Channel drop (kPa) | TC1 / TC2 / TC3 / TC4 (C) | Checks passed |
|---|---:|---:|---:|---:|---|---|
| coarse | 890 | 100 | 54,824 | 33.158 | 40.43 / 47.11 / 52.50 / 57.25 | True |
| medium | 890 | 100 | 171,600 | 33.475 | 40.63 / 47.48 / 52.86 / 57.62 | True |
| fine | 890 | 100 | 438,592 | 33.610 | 40.75 / 47.61 / 52.99 / 57.75 | True |
| depth_2p5 | 890 | 100 | 171,600 | 33.455 | 40.79 / 47.39 / 52.74 / 57.41 | True |
| depth_4p0 | 890 | 100 | 171,600 | 33.503 | 40.42 / 47.63 / 53.06 / 57.91 | True |
| width_1p588 | 890 | 100 | 171,600 | 33.475 | 40.62 / 47.48 / 52.86 / 57.61 | True |
| width_1p8 | 890 | 100 | 175,560 | 33.477 | 40.78 / 47.50 / 52.86 / 57.74 | True |
| q100_re226 | 226 | 100 | 171,600 | 5.490 | 55.48 / 67.43 / 78.64 / 88.44 | True |
| q100_re1454 | 1454 | 100 | 171,600 | 62.646 | 37.23 / 43.09 / 47.54 / 51.50 | True |
| q200_re442 | 442 | 200 | 171,600 | 9.975 | 77.48 / 95.00 / 109.90 / 122.96 | True |
| q200_re864 | 864 | 200 | 171,600 | 25.699 | 65.71 / 79.26 / 90.06 / 99.65 | True |
| q200_re1220 | 1220 | 200 | 171,600 | 41.372 | 60.92 / 72.95 / 82.28 / 90.64 | True |
| q200_re442_p200k | 442 | 200 | 171,600 | 9.975 | 77.48 / 95.00 / 109.90 / 122.96 | True |

Checks passed means residual targets, mass/heat conservation, and output stability passed. It does not mean agreement with experiments or mesh independence. Compact reports and convergence histories are included; case/data files are in the release archive.

## Mesh check

Medium-to-fine channel pressure-drop change: **0.400%**. Largest sensor change: **0.133 C**, or **0.496%** of temperature rise. Initial targets (<2% pressure, <1% temperature rise): **passed**. The operating-point and slot studies use the medium mesh; these mesh checks apply directly only to the Re=890 nominal baseline.

## Temperature comparison with the paper

Experimental values were manually digitized from Fig.7 symbol centers, not obtained as raw author data. Assigned reading uncertainty: +/-1 C, separate from the paper's reported thermocouple uncertainty below 0.3 C. Connected CFD points are guides between four sample locations, not a fully sampled temperature line.

| Case | CFD minus experiment at TC1 / TC2 / TC3 / TC4 (C) | Maximum absolute difference (C) |
|---|---|---:|
| q100_re226 | -1.52 / +0.83 / +0.84 / +1.04 | 1.52 |
| medium | +0.73 / +2.78 / +2.96 / +3.02 | 3.02 |
| q100_re1454 | +2.93 / +4.39 / +4.44 / +4.40 | 4.44 |
| q200_re442 | +4.18 / +7.30 / +7.30 / +9.16 | 9.16 |
| q200_re864 | +5.71 / +8.46 / +7.46 / +8.85 | 8.85 |
| q200_re1220 | +5.02 / +7.35 / +7.88 / +9.14 | 9.14 |

## Comparison with published numerical curves

The dashed curves and table below use separately digitized numerical predictions from Fig.7, with assigned reading uncertainty +/-1.5 C. This is a numerical-reproduction check, separate from comparison with experimental symbols. See digitization.md for the retained pixel calibration.

| Case | Largest difference from paper numerical curve at the four sensors (C) |
|---|---:|
| q100_re226 | 1.73 |
| medium | 1.39 |
| q100_re1454 | 0.75 |
| q200_re442 | 3.99 |
| q200_re864 | 4.04 |
| q200_re1220 | 3.74 |

## Reconstruction sensitivity

- depth_2p5: largest sensor change 0.206 C; channel pressure change -0.059% versus nominal at the same heat input and Re.
- depth_4p0: largest sensor change 0.290 C; channel pressure change +0.083% versus nominal at the same heat input and Re.
- width_1p588: largest sensor change 0.009 C; channel pressure change -0.000% versus nominal at the same heat input and Re.
- width_1p8: largest sensor change 0.148 C; channel pressure change +0.004% versus nominal at the same heat input and Re.

## Single-phase consistency and absolute pressure

The original atmospheric-outlet Re=442, 200 W/cm2 calculation is **numerically converged but thermodynamically inconsistent with stable single-phase water**: 424 fluid cell centers exceed local saturation temperature, by up to 11.22 K. Its temperatures are mathematical single-phase-model results, not a physically admissible atmospheric-pressure validation case.
A separate **200 kPa absolute outlet-pressure sensitivity** gives a minimum fluid-cell saturation margin of 9.02 K. The maximum water-contact wall temperature is 113.16 C versus saturation temperature 120.21 C at 200 kPa. This pressure is an engineering assumption; the paper does not specify its absolute outlet pressure. With the chosen incompressible, pressure-independent properties, changing the pressure reference should leave the temperature and channel pressure-drop predictions essentially unchanged.
The atmospheric run is retained to make this limitation visible. The pressure-sensitivity case does not establish the experimental pressure condition or remove the observed temperature discrepancies. The plot shows the single-phase numerical predictions; interpret the Re=442, 200 W/cm2 curve with this pressure caveat.

## Limits on interpretation

- Channel drop is DeltaP_ch. The experimental pressure taps include inlet/outlet plenums. Missing plenum dimensions prevent an exact total-pressure comparison; no hydraulic-validation claim is made.
- Slot depth and exact placement are reconstructed, not fully dimensioned in the source. The slot sweeps bracket assumptions; they are not measurement uncertainty bounds.
- Constant water density, cp, and conductivity use CoolProp at 15 C. Viscosity uses a local-temperature piecewise-linear liquid table. The paper says viscosity depends on mean temperature but does not provide enough implementation detail to reproduce its treatment exactly.
- Original copper k=400 W/(m K) differs slightly from the paper's explicit 401; polycarbonate k=0.2 agrees with its stated value (section 3.3, printed p.2558). Trapped-air k=0.026 remains an engineering assumption. See source_audit.md for the source correction and prepared material sensitivities.
- The paper's outlet treatment and Fluent pressure-outlet implementation differ. Material-property and outlet-formulation sensitivity remain outside this initial study; absolute outlet pressure was checked separately.
- Numerical verification and agreement trends do not establish an exact reproduction. Report the temperature discrepancies alongside the assumptions.

Source: https://doi.org/10.1016/S0017-9310(01)00337-4, Table 1, Figs.2-7, Eqs.11-23. Property source: https://coolprop.org/fluid_properties/fluids/Water.html. Detailed setup: reference_design.md.
