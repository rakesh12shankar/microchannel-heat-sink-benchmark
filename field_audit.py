"""Check fluid-cell saturation margins using saved Fluent fields."""
import h5py,numpy as np
from CoolProp.CoolProp import PropsSI
def phase_margins(folder,outlet_pressure):
 with h5py.File(folder/'solution.dat.h5') as f:
  c=f['results/1/phase-1/cells'];p=c['SV_P/1'];a=int(p.attrs['minId'][0])-1;b=int(p.attrs['maxId'][0]);t=c['SV_T/1'][a:b]
  ts=PropsSI('T','P',p[:]+outlet_pressure,'Q',np.zeros_like(t),'Water')
  return {'minimum_fluid_saturation_margin_K':float(np.min(ts-t)),'fluid_cells_above_saturation':int((t>ts).sum())}
