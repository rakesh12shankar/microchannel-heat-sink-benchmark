"""Rebuild point-comparison plots and a table from compact archived records."""
from pathlib import Path
import json,csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def main():
 out=ROOT/'.generated/analysis';out.mkdir(parents=True,exist_ok=True)
 records={p.stem:json.loads(p.read_text()) for p in (ROOT/'results/reference/records').glob('*.json')}
 with (ROOT/'data/digitization/figure7_digitized.csv').open() as f:exp=list(csv.DictReader(f))
 with (ROOT/'data/digitization/paper_numerical_digitized.csv').open() as f:pm=list(csv.DictReader(f))
 rows=[]
 for name,r in records.items():
  v=r['reports'];row={'case':name,'Re':r['Re'],'q_eff_W_cm2':r['q_eff_W_cm2'],'channel_dp_kPa':(v['pin']-v['pout'])/1000,'verified_converged':r['verified_converged']}
  row.update({f'TC{i}_C':v[f'tc{i}']-273.15 for i in range(1,5)});rows.append(row)
 with (out/'summary.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 fig,axs=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True);x=[5,16.588,28.176,39.764]
 for ax,q,cases in zip(axs,[100,200],[[(226,'q100_re226'),(890,'medium'),(1454,'q100_re1454')],[(442,'q200_re442'),(864,'q200_re864'),(1220,'q200_re1220')]]):
  for color,(reynolds,name) in zip(['#1c6a93','#ba5625','#2f7854'],cases):
   v=records[name]['reports'];ax.plot(x,[v[f'tc{i}']-273.15 for i in range(1,5)],color=color,label=f'Fluent Re={reynolds}')
   e=[r for r in exp if int(r['Re'])==reynolds and int(r['q_eff_W_cm2'])==q];m=[r for r in pm if int(r['Re'])==reynolds and int(r['q_eff_W_cm2'])==q]
   ax.errorbar(x,[float(r['T_experiment_C']) for r in e],yerr=1,fmt='o',color=color,capsize=3)
   ax.plot(x,[float(r['T_paper_numerical_C']) for r in m],'--',color=color,alpha=.7)
  ax.set(title=f'{q} W/cm²',xlabel='Sensor x (mm)',ylabel='Embedded copper temperature (°C)');ax.grid(alpha=.2);ax.legend(fontsize=8)
 fig.supxlabel('Markers: digitized experiment ±1°C; dashed: paper model. Atmospheric Re=442 high-heat case exceeds water saturation.',fontsize=8)
 fig.savefig(out/'temperature_comparison.png',dpi=180);plt.close(fig)
 print('Rebuilt compact summary and comparison plot for',len(rows),'archived cases in',out)
if __name__=='__main__':main()
