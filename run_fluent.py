"""Run one independent case from the published matrix in licensed Fluent 2024 R1."""
from pathlib import Path
import argparse,json,re,time,os
import ansys.fluent.core as pyfluent
from build_mesh import build,GENERATED
from fluent_setup import configure

ROOT=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',default='coarse');p.add_argument('--threads',type=int,default=1);p.add_argument('--output-dir',type=Path);a=p.parse_args()
 matrix=json.loads((ROOT/'config/cases.json').read_text());case=matrix[a.case];mesh=case['mesh']
 out=(a.output_dir or ROOT/'.generated/runs'/a.case).resolve()
 if out.exists() and any(out.iterdir()):raise RuntimeError('Output directory is not empty; choose a fresh --output-dir.')
 out.mkdir(parents=True,exist_ok=True)
 cfg=json.loads((ROOT/'config/meshes.json').read_text())[mesh]
 if not (GENERATED/mesh/'mesh.msh').exists():build(cfg['scale'],cfg['depth'],cfg['width'],mesh,cfg['cad'])
 audit=json.loads((GENERATED/mesh/'mesh_audit.json').read_text());assert audit['cells']==cfg['expected_cells']
 os.chdir(out)
 solver=None;history=[]
 try:
  solver=pyfluent.launch_fluent(product_version='24.1.0',mode='solver',precision='double',processor_count=a.threads,ui_mode='no_gui',start_timeout=180)
  transcript=out/'solver.trn';solver.transcript.start(str(transcript))
  solver.file.read_mesh(file_name=str(GENERATED/mesh/'mesh.msh'));solver.tui.mesh.check()
  inputs,reports=configure(solver,GENERATED/mesh,case)
  (out/'inputs.json').write_text(json.dumps({'case':case,'baseline_properties':inputs,'mesh':cfg},indent=2))
  solver.solution.initialization.hybrid_initialize();previous=None
  pattern=r'^\s*(\d+)\s+([0-9.]+e[+-]\d+)\s+([0-9.]+e[+-]\d+)\s+([0-9.]+e[+-]\d+)\s+([0-9.]+e[+-]\d+)\s+([0-9.]+e[+-]\d+)'
  for batch in range(20):
   solver.solution.run_calculation.iterate(iter_count=150)
   raw=solver.solution.report_definitions.compute(report_defs=reports);v={k:value[0] for part in raw for k,value in part.items()}
   rr=re.findall(pattern,transcript.read_text(errors='replace'),re.M);assert rr,'No residual rows recorded'
   res=dict(zip(['iteration','continuity','x_velocity','y_velocity','z_velocity','energy'],[int(rr[-1][0])]+[float(x) for x in rr[-1][1:]]))
   mass=abs(v['mass_in']+v['mass_out'])/abs(v['mass_in']);energy=abs(v['heat_net'])/abs(v['heat_in'])
   stable=False
   if previous:stable=max(abs(v[k]-previous[k]) for k in ['tc1','tc2','tc3','tc4','tout'])<.002 and abs(v['pin']-previous['pin'])/max(abs(v['pin']),1)<.0001
   ok=res['energy']<1e-9 and max(res[k] for k in ['continuity','x_velocity','y_velocity','z_velocity'])<1e-6 and mass<.001 and energy<.01 and stable
   record={'name':a.case,'Re':case['Re'],'q_eff_W_cm2':case['heat_flux_W_cm2'],'mesh':mesh,'outlet_absolute_pressure_Pa':case['outlet_absolute_pressure_Pa'],'reports':v,'residuals':res,'mass_imbalance_fraction':mass,'energy_imbalance_fraction':energy,'outputs_stable':stable,'verified_converged':ok}
   history.append(record);(out/'history.json').write_text(json.dumps(history,indent=2));print('CHECKPOINT',batch,record,flush=True)
   if ok:break
   previous=v
  solver.file.write_case_data(file_name=str(out/'solution.cas.h5'))
  (out/'result.json').write_text(json.dumps(record,indent=2))
  if not ok:raise RuntimeError('Numerical convergence checks did not all pass.')
  from CoolProp.CoolProp import PropsSI
  from field_audit import phase_margins
  record.update(phase_margins(out,case['outlet_absolute_pressure_Pa']))
  record['conservative_wall_saturation_margin_K']=float(PropsSI('T','P',case['outlet_absolute_pressure_Pa'],'Q',0,'Water'))-v['water_wall_tmax']
  (out/'result.json').write_text(json.dumps(record,indent=2));print('SAVED',out,flush=True)
 finally:
  if solver is not None:solver.exit()
if __name__=='__main__':main()
