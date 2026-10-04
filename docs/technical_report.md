# Technical report: microchannel heat-sink reconstruction

# Qu and Mudawar (2002): reconstructed Fluent benchmark

Source: Experimental and numerical study of pressure drop and heat transfer in a single-phase micro-channel heat sink, IJHMT 45, 2549-2565. DOI 10.1016/S0017-9310(01)00337-4. Local source in 01_Reference. This is independent of the 2025 canopy project.

## Geometry and traceability

Use the complete repeating unit cell in Fig. 3 and Table 1, including one full channel, copper half-fins on each side, the thick cover, and the three conduction-only air slots.

| Parameter | Value | Basis |
|---|---:|---|
| Channel length | 44.764 mm | Table 1 |
| Channel width / height | 0.231 / 0.713 mm | Table 1; prose also says 0.712 mm, use tabulated numerical domain |
| Half-fin width | 0.118 mm | Table 1 |
| Unit-cell width | 0.467 mm | 2(0.118)+0.231 |
| Copper depth below channel | 5.637 mm | Table 1 |
| Cover thickness | 12.7 mm | Table 1 |
| Total copper height | 6.350 mm | Sum |
| Number of channels | 21 | Section 2.2 |
| Thermocouple x | 5, 16.588, 28.176, 39.764 mm | Table 1 |
| Thermocouple z | 3.175 mm above bottom | Fig. 3 / Table 1: 3.175 mm below copper top |
| Air-slot width | 1.6 mm | Fig. 2 and section 2.2, rounded |
| Air-slot centers x | 10.794, 22.382, 33.970 mm | Reconstruction: midpoints between adjacent thermocouples |
| Air-slot depth | 3.175 mm nominal | ASSUMPTION from schematic alignment; not independently dimensioned |

Coordinates: x is flow, y spans the 0.467 mm pitch, z is upward from the copper bottom. Fluid bounds: y=0.118 to 0.349 mm; z=5.637 to 6.350 mm. Cover extends to z=19.050 mm. No sensor holes are cut, consistent with the paper's simplified numerical unit cell.

Sensitivity cases: slot depths 2.5, 3.175, 4.0 mm; slot widths 1.588, 1.6, 1.8 mm. These are reconstruction brackets, not experimental tolerances. Keep power fixed using actual heated copper-bottom area. Test depth first at fixed 1.6 mm width; width next at fixed nominal depth. Do not calibrate these values to improve agreement and then call the result independent validation.

## Loads and Fluent settings

Steady, 3D, double precision, pressure-based, laminar, energy on; no gravity or radiation. Water is the only flowing region. Copper, polycarbonate, and trapped slot air are conduction regions. Couple all contacting thermal interfaces. Side planes and nonloaded external boundaries are adiabatic. Apply top-cover convection h=10 W/(m2 K), ambient 298.15 K (Eq.15). Uniform water inlet, 288.15 K; pressure outlet 0 Pa gauge. Outlet treatment in Fluent is an implementation approximation to Eq.17; check its influence if results disagree near the exit.

Use paper's nominal planform area 1.0 cm x 4.48 cm for power: 448 W at 100 W/cm2; 896 W at 200 W/cm2. Unit-cell heat input = total/21. Heater flux = unit power / actual copper-bottom area, excluding air-slot bottoms (Eq.14). Do not simply apply the effective heat flux to the unit-cell bottom. Do not force 21 pitches to equal the rounded 10 mm physical width.

Baseline: Re=890, effective heat flux 100 W/cm2 (Fig.7a and section 3.3). Additional temperature cases: Re=226,1454 at 100 W/cm2 and Re=442,864,1220 at 200 W/cm2 (Fig.7). Re uses inlet properties, Dh=2wh/(w+h), and channel mean velocity. Match numerical material assumptions: constant properties except temperature-dependent water viscosity. The paper does not tabulate every property value or provide a complete viscosity implementation; record the selected property source and temperature in simulation inputs. Treat this uncertainty separately from geometry and mesh sensitivity.

## Verification and validation

Record mesh quality, solver residuals, mass balance, heater power, top-cover loss, outlet enthalpy flow, and stable engineering outputs. Perform a systematic three-mesh study before claiming mesh independence. Initial project criteria: mass imbalance <0.1%, energy imbalance <1%, medium-to-fine channel pressure-drop change <2%, thermocouple temperature-rise change <1%. These are project criteria, not criteria reported by the authors.

Extract temperatures at the four x positions, y=0.2335 mm, z=3.175 mm. Compare with Fig.7 experimental symbols; include digitization uncertainty and the paper's thermocouple uncertainty <0.3 C. Do not substitute maximum wall temperature.

Channel inlet-to-outlet pressure drop is DeltaP_ch only. Experimental Fig.4 uses deep-plenum pressure taps. Eq.18 adds contraction and expansion terms (Eqs.19-22). The paper says loss coefficients are close to unity but does not fully dimension plenum cross sections. Report channel drop and any approximate corrected total separately. Do not claim exact pressure validation from channel drop alone.

## Status

Initial study completed: five verified SolidWorks geometry variants and 13 saved Fluent simulations, including three meshes, four slot variants, six operating points (one overlaps the mesh baseline), and one absolute-pressure sensitivity. See results_overview.md for convergence, conservation, mesh checks, and comparison with digitized experimental and numerical temperatures.

Follow-up completed 2026-10-03: five property-treatment sensitivities and two demanding-point fine-mesh checks, for 20 total saved simulations. Both added mesh checks pass project criteria; the largest sensor change is 0.189 C and largest pressure change 0.462%. All seven added cases pass numerical and saturation consistency checks at the explicitly assumed 200 kPa outlet pressure. Exact validation remains qualified by the documented differences and missing source information.

The initial atmospheric outlet assumption produces above-saturation water in the Re=442, 200 W/cm2 case. A separate assumed 200 kPa absolute outlet pressure keeps fluid cells and water-contact walls below saturation. This does not establish the unreported experimental absolute pressure or eliminate temperature discrepancies. This project is a documented reconstruction, not a claim of exact validation.

Follow-up source audit (2026-10-03): section 3.3 explicitly states copper conductivity 401 W/(m K) and cover 0.2 W/(m K). Original copper 400 is retained in the original cases for traceability; a separate 401 sensitivity tests its effect. See source_audit.md and followup_results.md for property-treatment sensitivities, saved-wall saturation checks, and demanding-point mesh comparisons.


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


# Follow-up Fluent investigation

Completed and saved additional cases: **7 / 7**. Original solutions are retained. All added cases assume **200 kPa absolute outlet pressure**, keep original inlet velocity and heater power, and use the original density. Mean-property temperatures are frozen from the original case's arithmetic inlet/outlet bulk mean. These are sensitivity assumptions, not recovered author inputs.

## Findings and recommended use

The additional mesh checks **pass** the initial project criteria. Together with the baseline mesh and slot checks, these tests quantify numerical and reconstruction sensitivity at the tested points.
Correcting copper to the paper's 401 changes sensors by at most 0.043 C. Mean-temperature water k/cp changes them by at most 1.118 C in the high-heat diagnostic and 0.295 C at baseline. This accounts for only part of the discrepancy.
Uniform bulk-mean viscosity increases the high-heat temperatures and worsens agreement; the combined mean-property assumption also worsens agreement. These tests do not support selecting uniform viscosity as the explanation for the original difference.
Use this as a verified reconstruction with quantified sensitivities. Adopt the explicitly stated copper value 401 for future production setups. Retain the original cases and avoid selecting a property basis solely because it fits digitized curves. Exact reproduction remains limited by unreported property implementation, outlet treatment, and experimental conditions.
Further validation would benefit from original numerical property tables/code, absolute inlet/outlet pressures, plenum dimensions, and raw temperature/flow data. More mesh refinement alone is unlikely to explain the observed discrepancy when the demanding-point checks pass.

## Property assumptions

| Case | Maximum sensor change (C) | Channel pressure change | Maximum difference from experiment (C) | Maximum difference from paper model (C) |
|---|---:|---:|---:|---:|
| q200_re864_copper401 | 0.043 | -0.00% | 8.80 | 4.00 |
| q200_re864_mean_mu | 4.035 | +34.77% | 12.88 | 6.50 |
| q200_re864_mean_kcp | 1.118 | +0.42% | 7.73 | 3.37 |
| q200_re864_mean_all | 2.746 | +34.77% | 11.59 | 5.36 |
| medium_mean_kcp | 0.295 | +0.14% | 2.72 | 1.65 |

Copper401 changes only copper conductivity from 400 to the paper's explicitly stated 401 W/(m K). Mean_mu changes only viscosity to a uniform bulk-mean value. Mean_kcp changes water conductivity and heat capacity. Mean_all combines the latter two assumptions. Comparing these cases is a diagnostic; choosing the closest curve alone does not validate a property treatment.

## Demanding-point mesh checks

| Operating point | Medium-to-fine pressure change | Largest sensor change (C) | Largest relative sensor-rise change | Initial project criteria |
|---|---:|---:|---:|---|
| q200_re442 | 0.021% | 0.189 | 0.246% | Passed |
| q100_re1454 | 0.462% | 0.147 | 0.533% | Passed |

Comparisons use identical original material treatment. Moving the outlet pressure reference from atmospheric to 200 kPa has negligible effect under the chosen incompressible, pressure-independent properties, as checked by the original pressure-sensitivity pair. These checks support these operating points and do not prove every variant is mesh-independent.

## Numerical and phase consistency

| Case | Convergence checks | Mass imbalance | Energy imbalance | Minimum fluid saturation margin (K) | Conservative wall margin (K) |
|---|---|---:|---:|---:|---:|
| q200_re864_copper401 | True | 0.000009% | 0.000158% | 33.47 | 31.12 |
| q200_re864_mean_mu | True | 0.000009% | 0.008114% | 29.24 | 27.04 |
| q200_re864_mean_kcp | True | 0.000001% | 0.000057% | 34.53 | 32.25 |
| q200_re864_mean_all | True | 0.000009% | 0.005551% | 30.49 | 28.35 |
| medium_mean_kcp | True | 0.000003% | 0.000119% | 69.33 | 68.18 |
| q200_re442_fine | True | 0.000048% | 0.001209% | 8.18 | 6.88 |
| q100_re1454_fine | True | 0.000008% | 0.000672% | 74.87 | 74.03 |

Residual thresholds, conservation and stable engineering outputs are checked for each run. Saturation comparisons support only the assumed pressure and mathematical single-phase solution. They do not establish experimental pressure or predict boiling inception.

## Remaining limits

The exact mean-temperature viscosity implementation, reference temperatures for other water properties, absolute outlet pressure, and full plenum dimensions are unreported. The paper applies a second-derivative thermal condition at the channel exit; Fluent's pressure outlet uses its own thermal outflow treatment. No exact outlet-formulation reproduction is claimed. source_audit.md records source corrections and a conditional plenum-loss estimate derived from Eqs.18â€“22; those totals are assumption ranges, not validated pressure predictions.

The published numerical curve itself differs from the experimental symbols by up to **7.99 C** at these digitized sensor locations. Thus experimental discrepancy alone is not a measure of numerical reproduction. Experimental and paper-model values are digitized separately with assigned reading uncertainties +/-1 C and +/-1.5 C. No parameters have been fitted to those digitized values.

Saved case/data pairs are distributed separately in the v1.0.0 release archive. Compact records and convergence histories are in results/reference/. Case settings are in config/cases.json.
