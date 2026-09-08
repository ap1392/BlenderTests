import bpy,json,math
from mathutils import Vector
from pathlib import Path
blades=[]
for o in bpy.data.objects:
 if o.type!='MESH' or 'oak blade' not in o.name:continue
 pp=[o.matrix_world@Vector(v)for v in o.bound_box]
 blades.append((min(p.x for p in pp),max(p.x for p in pp),min(p.y for p in pp),max(p.y for p in pp),min(p.z for p in pp),max(p.z for p in pp)))
results=[]
for o in bpy.data.objects:
 if o.type!='MESH'or not o.name.startswith(('Ground drum luminaire housing','Social pod varied drum housing','Lobby drum housing')):continue
 pp=[o.matrix_world@v.co for v in o.data.vertices];p=sum(pp,Vector())/len(pp);top=max(q.z for q in pp);radius=max(math.hypot(q.x-p.x,q.y-p.y)for q in pp)
 gaps=[]
 for x0,x1,y0,y1,z0,z1 in blades:
  dx=max(x0-p.x,0,p.x-x1);dy=max(y0-p.y,0,p.y-y1)
  if dx*dx+dy*dy<=radius*radius and top-.4<z0<top+.7:gaps.append(z0-top)
 results.append({'fixture':o.name,'minimum_blade_clearance_m':min(gaps)if gaps else None})
bad=[r for r in results if r['minimum_blade_clearance_m']is not None and r['minimum_blade_clearance_m']<-.001]
report={'fixture_count':len(results),'blade_objects_checked':len(blades),'intersections':bad,'fixtures':results,'scope':'Circle-versus-blade bounding-envelope test at each fixture, including distinct ground and gallery ceiling elevations.'}
Path('/Users/aditya2610/Desktop/Projects3/BlenderTests/references/fidelity/calibration/fixture_clearance_audit.json').write_text(json.dumps(report,indent=2));print('Fixtures',len(results),'blade envelopes',len(blades),'intersections',bad)
assert not bad
