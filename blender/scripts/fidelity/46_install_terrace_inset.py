exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name in ['L2 continuous public gallery slab','L2 documented terrace warm grey floor']or o.name.startswith('L2 documented terrace integrated floor fascia'))
d=json.loads((ROOT/'references/fidelity/calibration/l2_terrace_union.json').read_text());C='Architecture'
def volume(name,p,top,thick,ma):
 xy=p['vertices'];N=len(xy);vs=[(x,y,top-thick)for x,y in xy]+[(x,y,top)for x,y in xy];fs=[tuple(reversed(f))for f in p['triangles']]+[tuple(i+N for i in f)for f in p['triangles']]
 for ring in p['rings']:
  for a,b in zip(ring,ring[1:]+ring[:1]):fs.append((a,b,b+N,a+N))
 ob=mesh(name,vs,fs,ma);finish(ob);return ob
volume('L2 continuous public gallery slab',d['floor'],H,.42,white)
volume('L2 documented terrace warm grey floor',d['terrace'],H+.008,.004,bpy.data.materials['Write-up warm grey carpet'])
for ring in d['floor']['rings']:
 path=[tuple(d['floor']['vertices'][i])for i in ring];path.append(path[0]);finish(ribbon('L2 documented terrace integrated floor fascia',path,[H-.635]*len(path),.638,.04,white),True)
bpy.context.scene['terrace_intersection_correction']='Floor edge inset200mm into280mm concrete wall to remove coincident outer surfaces found in2048px validation.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
