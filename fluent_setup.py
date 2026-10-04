import json
from pathlib import Path
def configure(solver,mesh_path,case):
    solver.setup.models.energy.enabled=True
    solver.setup.models.viscous.model='laminar'
    solver.setup.materials.fluid.create('water_benchmark')
    water=solver.setup.materials.fluid['water_benchmark']
    water.viscosity.option='piecewise-linear'
    from CoolProp.CoolProp import PropsSI
    import numpy as np
    Tin=288.15;Re=case['Re'];Q=(448/21)*(case['heat_flux_W_cm2']/100)
    rho=PropsSI('D','T',Tin,'P',101325,'Water');cp=PropsSI('C','T',Tin,'P',101325,'Water');kf=PropsSI('L','T',Tin,'P',101325,'Water');muin=PropsSI('V','T',Tin,'P',101325,'Water')
    Dh=2*.000231*.000713/(.000231+.000713);uin=Re*muin/(rho*Dh)
    inputs={'Re':Re,'Tin_K':Tin,'unit_power_W':Q,'rho':rho,'cp':cp,'kf':kf,'mu_in':muin,'Dh_m':Dh,'uin_m_s':uin,'property_basis':'CoolProp liquid water at 15 C, 101325 Pa; viscosity is local T-dependent table','copper_k':400.,'cover_k':.2,'slot_air_k':.026,'solid_property_basis':'Engineering assumptions, not tabulated in paper'}
    for key,value in {'density':rho,'specific_heat':cp,'thermal_conductivity':kf}.items():getattr(water,key).set_state({'option':'constant','value':value})
    water.viscosity.piecewise_linear=[[float(t),float(PropsSI('V','T',float(t),'Q',0,'Water'))] for t in np.arange(273.15,403.16,5)]
    solver.setup.cell_zone_conditions.fluid['water'].material='water_benchmark'
    for zone,k,density,heatcap in [('copper',case.get('copper_k',400),8960,385),('cover',.2,1200,1200),('airslots',.026,1.2,1006)]:
        mat=zone+'_benchmark';solver.setup.materials.solid.create(mat);s=solver.setup.materials.solid[mat]
        s.thermal_conductivity.value=k;s.density.value=density;s.specific_heat.value=heatcap
        solver.setup.cell_zone_conditions.solid[zone].material=mat
    solver.setup.boundary_conditions.velocity_inlet['inlet'].momentum.velocity.value=uin
    solver.setup.boundary_conditions.velocity_inlet['inlet'].thermal.t.value=Tin
    solver.setup.boundary_conditions.pressure_outlet['outlet'].thermal.t0.value=Tin
    audit=json.loads((mesh_path/'mesh_audit.json').read_text())
    solver.setup.boundary_conditions.wall['heater'].thermal.q.value=Q/audit['heater_area_m2']
    top=solver.setup.boundary_conditions.wall['ambient_top'].thermal
    top.thermal_bc='Convection';top.h.value=10;top.tinf.value=298.15
    solver.solution.methods.p_v_coupling.flow_scheme='Coupled'
    solver.solution.methods.discretization_scheme={'pressure':'second-order','mom':'second-order-upwind','temperature':'second-order-upwind'}
    for n in ['continuity','x-velocity','y-velocity','z-velocity']:solver.solution.monitor.residual.equations[n].absolute_criteria=1e-6
    solver.solution.monitor.residual.equations['energy'].absolute_criteria=1e-9
    reports={'tout':('surface-massavg','temperature',['outlet']),'pin':('surface-areaavg','pressure',['inlet']),'pout':('surface-areaavg','pressure',['outlet']),'heater_tmean':('surface-areaavg','temperature',['heater']),'heater_tmax':('surface-facetmax','temperature',['heater'])}
    for name,(typ,field,surfaces) in reports.items():
        solver.solution.report_definitions.surface.create(name);r=solver.solution.report_definitions.surface[name];r.report_type=typ;r.field=field;r.surface_names=surfaces
    fluxes={'mass_in':('flux-massflow',['inlet']),'mass_out':('flux-massflow',['outlet']),'heat_in':('flux-heattransfer',['heater']),'heat_top':('flux-heattransfer',['ambient_top'])}
    for name,(typ,surfaces) in fluxes.items():
        solver.solution.report_definitions.flux.create(name);r=solver.solution.report_definitions.flux[name];r.report_type=typ;r.boundaries=surfaces
    
    
    for index,xx in enumerate([.005,.016588,.028176,.039764],1):
        name='tc'+str(index)
        solver.results.surfaces.point_surface.create(name)
        solver.results.surfaces.point_surface[name].point=[xx,.0002335,.003175]
        solver.solution.report_definitions.surface.create(name)
        r=solver.solution.report_definitions.surface[name];r.report_type='surface-vertexavg';r.field='temperature';r.surface_names=[name]
        reports[name]=('surface-vertexavg','temperature',[name])
    solver.solution.report_definitions.flux.create('heat_net')
    r=solver.solution.report_definitions.flux['heat_net'];r.report_type='flux-heattransfer';r.boundaries=['heater','ambient_top','inlet','outlet']
    fluxes['heat_net']=('flux-heattransfer',['heater','ambient_top','inlet','outlet'])
    
    
    solver.setup.general.operating_conditions.operating_pressure=case['outlet_absolute_pressure_Pa']
    if case.get('viscosity')=='constant':water.viscosity.set_state({'option':'constant','value':case['mu']})
    for key in ['thermal_conductivity','specific_heat']:
        if key in case:getattr(water,key).set_state({'option':'constant','value':case[key]})
    solver.solution.report_definitions.surface.create('water_wall_tmax')
    r=solver.solution.report_definitions.surface['water_wall_tmax'];r.report_type='surface-facetmax';r.field='temperature';r.surface_names=['coupled_copper_water','coupled_cover_water'];reports['water_wall_tmax']=None
    for name in solver.setup.boundary_conditions.wall.get_object_names():
        if name.startswith('coupled_'):assert solver.setup.boundary_conditions.wall[name].thermal.thermal_bc()=='Coupled'
    solver.solution.run_calculation.pseudo_time_settings.time_step_method.time_step_size_scale_factor=5
    solver.solution.run_calculation.pseudo_time_settings.time_step_method.time_solid_scale_factor=5
    return inputs,list(reports)+list(fluxes)
