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

The exact mean-temperature viscosity implementation, reference temperatures for other water properties, absolute outlet pressure, and full plenum dimensions are unreported. The paper applies a second-derivative thermal condition at the channel exit; Fluent's pressure outlet uses its own thermal outflow treatment. No exact outlet-formulation reproduction is claimed. source_audit.md records source corrections and a conditional plenum-loss estimate derived from Eqs.18–22; those totals are assumption ranges, not validated pressure predictions.

The published numerical curve itself differs from the experimental symbols by up to **7.99 C** at these digitized sensor locations. Thus experimental discrepancy alone is not a measure of numerical reproduction. Experimental and paper-model values are digitized separately with assigned reading uncertainties +/-1 C and +/-1.5 C. No parameters have been fitted to those digitized values.

Saved case/data pairs are distributed separately in the v1.0.0 release archive. Compact records and convergence histories are in results/reference/. Case settings are in config/cases.json.
