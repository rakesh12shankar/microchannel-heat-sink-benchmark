# Reproduction guide

## Inspect the archived study without commercial software

Install requirements.txt, then run `python run_analysis.py` and `python run_validation.py` from the repository root. Analysis regenerates compact plots/tables in `.generated/analysis`; validation checks the 20 supplied records and physical/numerical interpretation. It does not rerun CFD or independently validate the experiment.

## Regenerate one CFD case

Install requirements-simulation.txt in a Python 3.12 environment. Fluent 2024 R1 must be installed and licensed. Run `python run_fluent.py --case coarse --threads 1`. Select any named case in config/cases.json. The command builds the mesh from the matching verified STEP file, configures Fluent, initializes, solves, checks residuals/conservation/stability, and saves case/data plus records under `.generated/runs/<case>`. No author PDF is needed at runtime.

Existing generated runs are protected: choose a fresh output directory with `--output-dir PATH` to repeat a case. Each case launches a separate solver session; no previous case is required. The root build_mesh.py can also run directly with mesh scale, slot dimensions and CAD variant arguments.

The original results were obtained across development sessions with warm-start interpolation in several cases. The published runner uses fresh hybrid initialization. It preserves physics and sampling but may require a different iteration count. Its acceptance tolerances and actual packaging smoke-run evidence are recorded in milestone_status.md.

## Regenerate CAD

Use Windows PowerShell 5.1, SolidWorks 2019, and the installed interop assembly/Part template paths in build_geometry.ps1. Example: `powershell.exe -File build_geometry.ps1 -Variant rebuilt_nominal -OutputRoot .generated/cad`. Paths are installation-specific and may need editing for other versions. CAD uses imported Boolean bodies through the SolidWorks modeler API; it is script-controlled rather than a sketch-feature parameter tree. Existing variant names are protected against overwriting.

## Retrieve full solver solutions

The v1.0.0 release contains `fluent-solutions-v1.0.0.zip`, with each original solution.cas.h5 and solution.dat.h5 pair, mesh audit records and a checksum manifest. Fluent is needed to open/review these solutions; it is not needed to inspect the public CSV/JSON outputs or rebuild summary plots. The release archive excludes license information, transcripts, publisher files and private workspace material.

## Evidence map

- Original 13 cases: results/reference/simulation_summary.csv and records/.
- Seven additions: followup_simulation_summary.csv and records/.
- Actual convergence checkpoints: histories/; automatic solver stopping may make successive checkpoints fewer than 150 iterations apart.
- Water-wall phase checks and conditional plenum estimates: followup_source_and_field_audit.csv and docs/source_audit.md.
- CAD partition and dimensions: data/cad/*/CAD_Checks.txt and generated mesh_audit.json.
- Original file-pair audit: completion_audit.json; publication package hashes: UPLOAD_MANIFEST.json.

All reported CFD fields were solved by Fluent. Python generates geometry/meshes, orchestrates the commercial solver, and reads outputs; it is not a substitute CFD solver. The field contour figure comes from the original saved Fluent solution and is supplied as an archived image, not regenerated from the compact records.

The publication smoke check used one Fluent process. Increase `--threads` for licensed parallel execution. See results/publication_smoke/ for the fresh-run comparison.
