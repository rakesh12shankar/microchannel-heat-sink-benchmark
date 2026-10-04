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
