# Follow-up audit: source, material properties, pressure and saved fields

This audit uses the original saved Fluent solutions. Additional simulation tests are reported in followup_results.md.

## Source corrections and confirmed inputs

- Copper conductivity is explicitly **401 W/(m K)** and cover conductivity **0.2 W/(m K)** in the paper, printed page 2558 (PDF page 10), section 3.3. The initial calculation used copper 400 and cover 0.2. The earlier statement that both values were unreported was incorrect. The original cases remain unchanged for traceability; a 401 sensitivity is prepared.
- Section 2.3 and Eqs.1–3 confirm electrical power divided by planform area, 21 channels, 15 C inlet, and Reynolds number using inlet viscosity. The existing load and inlet-speed definitions follow these statements.
- Section 2.4 estimates ambient heat loss below 1%. Reducing input power by 1% would reduce the temperature rise by about 1% in a fixed-property linear model; that scale alone is too small to explain a 9 C discrepancy. This is a scale estimate, not a new Fluent run.
- Section 3.1 says temperature-dependent viscosity based on mean temperature but does not define which mean or give an implementation. Our local-temperature viscosity table is one interpretation. A uniform viscosity at the arithmetic inlet/outlet bulk mean is another sensitivity assumption; it is not asserted to be the authors' implementation.
- Table 1 provides Hch=713 micrometers, while the experimental description says 712. We retain the numerical-model Table 1 value. Thermocouple positions and bottom-area power conversion remain as audited in the benchmark definition.

## Property temperature comparison

The arithmetic bulk mean below uses the original solved outlet temperature. Values use CoolProp at 200 kPa; inlet velocity and original inlet-property Reynolds number are held fixed in the prepared sensitivity runs. Density stays at its original constant value.

| Case | Bulk mean (C) | Mean water k (W/m K) | Change from inlet k | Mean cp (J/kg K) | Mean viscosity (mPa s) |
|---|---:|---:|---:|---:|---:|
| q100_re226 | 35.98 | 0.62313 | +5.83% | 4179.0 | 0.7053 |
| medium | 20.33 | 0.59865 | +1.67% | 4183.5 | 0.9936 |
| q100_re1454 | 18.26 | 0.59495 | +1.04% | 4185.0 | 1.0457 |
| q200_re442 | 36.46 | 0.62378 | +5.94% | 4179.0 | 0.6987 |
| q200_re864 | 25.98 | 0.60816 | +3.29% | 4180.7 | 0.8705 |
| q200_re1220 | 22.77 | 0.60287 | +2.39% | 4182.1 | 0.9370 |

These property differences identify useful sensitivity directions; they do not quantify their resulting temperature or pressure-drop changes until Fluent runs. The bulk mean is frozen from each reference case to isolate the changed assumptions.

## Wall saturation check from saved Fluent face temperatures

Wall maxima are extracted from SV_T on both water-contact interface face zones in the saved HDF5 files. Comparison uses saturation at the assumed outlet absolute pressure, a conservative reference relative to the higher upstream pressure.

| Case | Maximum water-contact wall (C) | Outlet absolute pressure (kPa) | Conservative saturation margin (K) |
|---|---:|---:|---:|
| q100_re226 | 84.21 | 101.325 | 15.77 |
| medium | 52.33 | 101.325 | 47.64 |
| q100_re1454 | 46.04 | 101.325 | 53.94 |
| q200_re442 | 113.16 | 101.325 | -13.19 |
| q200_re864 | 89.10 | 101.325 | 10.87 |
| q200_re1220 | 79.82 | 101.325 | 20.16 |
| q200_re442_p200k | 113.16 | 200.000 | 7.05 |

The atmospheric Re=442 high-heat case fails this check; the separately assumed 200 kPa case passes. Saturation pressure at its hottest water-contact wall (113.16 C) is about 159.3 kPa. An outlet pressure above that value is a conservative sufficient condition for this wall-temperature check because upstream pressure is higher. It is not an inferred experimental pressure or a boiling-inception prediction.

## Conditional plenum-loss estimate

For symmetric inlet/outlet plenum areas, equal inlet/outlet mean channel speeds under constant density, and all four loss coefficients set to 1 (the paper says close to unity), the kinetic-energy terms in Eqs.19–22 telescope to zero. Added loss becomes rho*(U_channel^2 + U_shallow^2). Writing r=U_shallow/U_channel gives added loss rho*U_channel^2*(1+r^2).

The following conditional range assumes 0 <= r <= 1, consistent with a shallow plenum whose flow area is at least the combined channel area. Neither r nor exact coefficients are measured here. This is an assumption range, not an experimental uncertainty interval or CFD plenum simulation.

| Case | Channel drop (kPa) | Added loss, r=0 to 1 (kPa) | Conditional total (kPa) |
|---|---:|---:|---:|
| q100_re226 | 5.490 | 0.543 to 1.087 | 6.034 to 6.577 |
| medium | 33.475 | 8.426 to 16.851 | 41.901 to 50.327 |
| q100_re1454 | 62.646 | 22.488 to 44.976 | 85.135 to 107.623 |
| q200_re442 | 9.975 | 2.078 to 4.156 | 12.053 to 14.131 |
| q200_re864 | 25.699 | 7.941 to 15.881 | 33.639 to 41.580 |
| q200_re1220 | 41.372 | 15.832 to 31.665 | 57.204 to 73.036 |

Exact hydraulic validation still requires plenum geometry, coefficient treatment, and matching measured pressure data. These estimates show why comparing channel pressure alone with the plotted total pressure is insufficient.

## Prepared Fluent follow-up matrix

At Re=864 and 200 W/cm2: copper 401 alone; uniform mean-temperature viscosity alone; mean-temperature water k/cp alone; mean viscosity plus mean k/cp. At Re=890 and 100 W/cm2: mean k/cp. Fine-mesh checks: Re=442 at 200 W/cm2 and Re=1454 at 100 W/cm2. All seven additional cases use an explicitly assumed 200 kPa absolute outlet pressure.

Initial Fluent launches on 2026-10-03 failed with "Unexpected license problem; exiting." After the user confirmed the setup had been repaired, the normal four-process launch succeeded. Additional simulation results are reported separately in followup_results.md. The published runner is run_fluent.py. Development transcripts and failed launch attempts remain in the local research archive.
