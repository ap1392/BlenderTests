exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Keep the real wood soffit visible: only the perimeter fascia deepens, not the entire slab.
for ob in bpy.data.objects:
 if 'continuous public gallery slab'in ob.name and ob.get('fascia_depth_v32'):
  bottom=min(v.co.z for v in ob.data.vertices)
  for v in ob.data.vertices:
   if abs(v.co.z-bottom)<.001:v.co.z+=.20
  del ob['fascia_depth_v32'];finish(ob)
C='Architecture';remove_where(lambda o:o.name.startswith('Continuous perimeter white fascia'))
data=json.loads((ROOT/'references/fidelity/calibration/public_floor_union.json').read_text())
for z in FLOORS[1:]:
 for part in data['parts']:
  for ring in part['rings']:
   path=[tuple(part['vertices'][i])for i in ring];path.append(path[0]);ob=ribbon('Continuous perimeter white fascia',path,[z-.635]*len(path),.638,.04,white);finish(ob,True)
# Shared lower/upper transition has the same 1.52m clear width.
# Rescale only transverse lower-stair coordinates, preserving centreline, pitch, and endpoints.
old=path_resample(smooth(P([(875.6,428.5),(870,441),(860,457),(847,472),(835,484)])+[(2.24*cos(math.radians(-47)),2.24*sin(math.radians(-47)))],12),31)
fine=path_resample(smooth(old,4),181)
def deform(v,centers):
 p=min(centers,key=lambda p:(v.x-p[0])**2+(v.y-p[1])**2);v.x=p[0]+(v.x-p[0])*(1.52/1.92);v.y=p[1]+(v.y-p[1])*(1.52/1.92)
for ob in bpy.data.objects:
 if not ob.name.startswith(('Fidelity lower stair tread','Lower stair traction','Lower stair continuous','Lower stair clear glass','Lower stair inset handrail','Lower stair recessed warm')):continue
 if ob.get('width_152_v33'):continue
 if ob.type=='MESH':
  for v in ob.data.vertices:deform(v.co,fine)
  finish(ob)
 elif ob.type=='CURVE':
  for sp in ob.data.splines:
   for p in sp.points:deform(p.co,fine)
 ob['width_152_v33']=True
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
