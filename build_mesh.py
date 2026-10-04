"""Conformal Cartesian hex mesh of the audited SolidWorks unit-cell geometry.

Coordinates in SI. Geometry is exactly rectilinear; the CAD STEP body bounds and
volumes are independently checked before meshing. Fluent's right-hand normal points
toward c0. No Fluent simulation is performed by this mesh writer.
"""
from pathlib import Path
import argparse, json, math
from collections import defaultdict
import numpy as np

ROOT=Path(__file__).resolve().parent
GENERATED=ROOT/'.generated/meshes';GENERATED.mkdir(parents=True,exist_ok=True)
NAMES={1:'water',2:'copper',3:'cover',4:'airslots'}

def build(scale=1.,depth=.003175,width=.0016,name='coarse',cad='nominal'):
    L,W,H=.044764,.000467,.01905
    centers=[.010794,.022382,.033970]
    slots=[(c-width/2,c+width/2) for c in centers]
    # Independent STEP audit: OCC returns millimeters from the SolidWorks STEP.
    import gmsh
    gmsh.initialize();gmsh.option.setNumber('General.Terminal',0)
    cad_dir=ROOT/'data/cad'/cad
    cad_file=cad_dir/('Qu_'+cad+'.STEP')
    if not cad_file.exists():cad_file=cad_dir/'Qu_UnitCell.STEP'
    gmsh.model.occ.importShapes(str(cad_file))
    gmsh.model.occ.synchronize()
    actual=[]
    for dim,tag in gmsh.model.getEntities(3):
        actual.append({'volume_m3':gmsh.model.occ.getMass(3,tag)*1e-9,
                       'bounds_m':[v*.001 for v in gmsh.model.getBoundingBox(3,tag)]})
    gmsh.finalize()
    target_vol=[L*.000231*.000713,L*W*.00635-L*.000231*.000713-3*width*W*depth,L*W*.0127,3*width*W*depth]
    expected_individual=[target_vol[0],target_vol[1],target_vol[2]]+[width*W*depth]*3
    assert len(actual)==6
    assert np.allclose(sorted(a['volume_m3'] for a in actual),sorted(expected_individual),rtol=1e-6,atol=1e-15),'CAD volume mismatch'
    bounds=np.array([a['bounds_m'] for a in actual])
    assert np.allclose(bounds[:,:3].min(axis=0),[0,0,0],atol=2e-9),'CAD origin mismatch'
    assert np.allclose(bounds[:,3:].max(axis=0),[L,W,H],atol=2e-9),'CAD extent mismatch'
    def segment(a,b,n,grading=1.):
        n=max(1,int(round(n*scale)))
        weights=np.geomspace(1,grading,n);edges=np.r_[0,np.cumsum(weights)/weights.sum()]
        return a+(b-a)*edges
    def join(parts):return np.concatenate([p[:-1] for p in parts]+[parts[-1][-1:]])
    xb=[0,.0001,.0004,.001,.002]+[v for pair in slots for v in pair]+[L]
    xb=sorted(set(xb))
    x=join([segment(a,b,max(2,math.ceil((b-a)/.00055))) for a,b in zip(xb[:-1],xb[1:])])
    y=join([segment(0,.000118,3),segment(.000118,.000349,8),segment(.000349,W,3)])
    z=join([segment(0,depth,8),segment(depth,.005637,8,.2),segment(.005637,.00635,16),segment(.00635,H,12,25)])
    nx,ny,nz=len(x)-1,len(y)-1,len(z)-1
    mids=[(a[:-1]+a[1:])/2 for a in [x,y,z]]
    regions=np.empty((nx,ny,nz),dtype=int)
    for i,cx in enumerate(mids[0]):
      for j,cy in enumerate(mids[1]):
       for k,cz in enumerate(mids[2]):
        r=3 if cz>.00635 else (1 if cz>.005637 and .000118<cy<.000349 else 2)
        if cz<depth and any(a<cx<b for a,b in slots):r=4
        regions[i,j,k]=r
    ids=np.zeros_like(regions);ranges={};vols={};last=0
    cellvol=np.diff(x)[:,None,None]*np.diff(y)[None,:,None]*np.diff(z)[None,None,:]
    for r in NAMES:
        mask=regions==r;n=int(mask.sum());ids[mask]=np.arange(last+1,last+n+1)
        ranges[r]=(last+1,last+n);last+=n;vols[NAMES[r]]=float(cellvol[mask].sum())
    assert np.allclose([vols[NAMES[r]] for r in NAMES],target_vol,rtol=1e-10,atol=1e-17)
    def node(i,j,k):return (i*(ny+1)+j)*(nz+1)+k+1
    faces=defaultdict(list);types={}
    def add(nodes,lo,hi,boundary):
        r0=int(regions[lo]) if lo else 0;r1=int(regions[hi]) if hi else 0
        if r0 and r1:
            label='interior_'+NAMES[r0] if r0==r1 else 'coupled_'+'_'.join(sorted([NAMES[r0],NAMES[r1]]))
            typ=2 if r0==r1 else 3
        else:
            r=r0 or r1
            if boundary=='xmin' and r==1:label,typ='inlet',10
            elif boundary=='xmax' and r==1:label,typ='outlet',5
            elif boundary=='zmin' and r==2:label,typ='heater',3
            elif boundary=='zmax':label,typ='ambient_top',3
            else:label,typ='adiabatic_'+NAMES[r]+'_'+boundary,3
        c0=int(ids[hi]) if hi else 0;c1=int(ids[lo]) if lo else 0
        if c0==0:nodes=nodes[::-1];c0,c1=c1,0
        faces[label].append((*nodes,c0,c1));types[label]=typ
    for i in range(nx+1):
      for j in range(ny):
       for k in range(nz):
        add([node(i,j,k),node(i,j+1,k),node(i,j+1,k+1),node(i,j,k+1)],(i-1,j,k) if i else None,(i,j,k) if i<nx else None,'xmin' if i==0 else 'xmax')
    for i in range(nx):
      for j in range(ny+1):
       for k in range(nz):
        add([node(i,j,k),node(i,j,k+1),node(i+1,j,k+1),node(i+1,j,k)],(i,j-1,k) if j else None,(i,j,k) if j<ny else None,'ymin' if j==0 else 'ymax')
    for i in range(nx):
      for j in range(ny):
       for k in range(nz+1):
        add([node(i,j,k),node(i+1,j,k),node(i+1,j+1,k),node(i,j+1,k)],(i,j,k-1) if k else None,(i,j,k) if k<nz else None,'zmin' if k==0 else 'zmax')
    out=GENERATED/name;out.mkdir(exist_ok=True)
    with (out/'mesh.msh').open('w') as f:
        f.write('(0 "Qu Mudawar reconstructed unit cell SI hex mesh")\n(2 3)\n')
        nodes=(nx+1)*(ny+1)*(nz+1)
        f.write(f'(10 (0 1 {nodes:x} 0 3))\n(10 (a 1 {nodes:x} 1 3)(\n')
        for xx in x:
         for yy in y:
          for zz in z:f.write(f'{xx:.15g} {yy:.15g} {zz:.15g}\n')
        f.write('))\n'+f'(12 (0 1 {last:x} 0))\n')
        for r,(a,b) in ranges.items():
            f.write(f'(12 ({r:x} {a:x} {b:x} 1 4))\n(39 ({r} {"fluid" if r==1 else "solid"} {NAMES[r]} 1)())\n')
        nf=sum(map(len,faces.values()));f.write(f'(13 (0 1 {nf:x} 0))\n');first=1
        for zid,(label,flist) in enumerate(faces.items(),20):
            typ=types[label];f.write(f'(13 ({zid:x} {first:x} {first+len(flist)-1:x} {typ:x} 4)(\n')
            for row in flist:f.write(' '.join(f'{v:x}' for v in row)+'\n')
            f.write('))\n');kind={2:'interior',3:'wall',5:'pressure-outlet',10:'velocity-inlet'}[typ]
            f.write(f'(39 ({zid} {kind} {label} 1)())\n');first+=len(flist)
    audit={'cells':last,'dimensions_cells':[nx,ny,nz],'volumes_m3':vols,'cad_audit':actual,'scale':scale,'slot_depth_m':depth,'slot_width_m':width,'heater_area_m2':W*(L-3*width),'water_area_m2':.000231*.000713,'cad_variant':cad}
    (out/'mesh_audit.json').write_text(json.dumps(audit,indent=2))
    print(json.dumps(audit,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=1);p.add_argument('--depth',type=float,default=.003175);p.add_argument('--width',type=float,default=.0016);p.add_argument('--name',default='coarse');p.add_argument('--cad',default='nominal');a=p.parse_args()
    build(a.scale,a.depth,a.width,a.name,a.cad)
