"""Audit archived convergence records and tabulated sensitivity claims."""
from pathlib import Path
import json,csv,math
ROOT=Path(__file__).resolve().parent
def main():
 cases=json.loads((ROOT/'config/cases.json').read_text());assert len(cases)==20
 records={}
 for name in cases:
  r=json.loads((ROOT/'results/reference/records'/(name+'.json')).read_text());records[name]=r
  assert r['verified_converged'] and r['outputs_stable'],name
  assert r['mass_imbalance_fraction']<.001 and r['energy_imbalance_fraction']<.01,name
  res=r['residuals'];assert res['energy']<1e-9 and max(res[k] for k in ['continuity','x_velocity','y_velocity','z_velocity'])<1e-6,name
  assert all(math.isfinite(float(v)) for v in r['reports'].values()),name
 for medium,fine in [('medium','fine'),('q200_re442','q200_re442_fine'),('q100_re1454','q100_re1454_fine')]:
  m,f=records[medium]['reports'],records[fine]['reports'];dp=abs(f['pin']-m['pin'])/abs(f['pin'])*100
  tr=max(abs(f[f'tc{i}']-m[f'tc{i}'])/abs(f[f'tc{i}']-288.15)*100 for i in range(1,5));assert dp<2 and tr<1
 with (ROOT/'results/reference/simulation_summary.csv').open() as f:rows={r['case']:r for r in csv.DictReader(f)}
 assert int(rows['q200_re442']['fluid_cells_above_saturation'])>0
 assert int(rows['q200_re442_p200k']['fluid_cells_above_saturation'])==0
 with (ROOT/'results/reference/followup_simulation_summary.csv').open() as f:
  for r in csv.DictReader(f):assert float(r['minimum_fluid_saturation_margin_K'])>0 and float(r['conservative_wall_saturation_margin_K'])>0
 print('PASS: 20 numerical records; three mesh comparisons; retained phase-failure flag; seven follow-up phase checks. This is a record audit, not experimental validation.')
if __name__=='__main__':main()
