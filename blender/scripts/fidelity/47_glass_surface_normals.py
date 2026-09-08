exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Bent glass is concentric, not an averaged faceted optical surface. Independent
# panel-end smoothing had up to1degree error, magnified by reflection/refraction.
count=0
for ob in bpy.data.objects:
 if not ob.name.startswith('Radial stair glass panel'):continue
 m=ob.data
 for i in range(0,len(m.vertices),4):
  p=m.vertices[i].co;r=math.hypot(p.x,p.y);n=Vector((p.x/r,p.y/r,0))
  for j in [1,2]:m.vertices[i+j].co.x=n.x*(r-.013);m.vertices[i+j].co.y=n.y*(r-.013)
 finish(ob)
 normals=[None]*len(m.loops)
 for f in m.polygons:
  center=sum((m.vertices[m.loops[li].vertex_index].co for li in f.loop_indices),Vector())/len(f.loop_indices);radial=Vector((center.x,center.y,0)).normalized();side=abs(f.normal.dot(radial))>.9;f.use_smooth=side
  sign=1 if f.normal.dot(radial)>0 else -1
  for li in f.loop_indices:
   p=m.vertices[m.loops[li].vertex_index].co;normals[li]=tuple(Vector((p.x,p.y,0)).normalized()*sign)if side else tuple(f.normal)
 m.normals_split_custom_set(normals);count+=1
# Lower panels use the shared full-flight tangent, not each short panel's isolated
# endpoint normal; this keeps refraction consistent across neighboring panels.
path=path_resample(smooth(P([(875.6,428.5),(870,441),(860,457),(847,472),(835,484)])+[(2.24*cos(math.radians(-47)),2.24*sin(math.radians(-47)))],12),31)
path=path_resample(smooth(path,4),181)
for ob in bpy.data.objects:
 if not ob.name.startswith('Lower stair clear glass panel'):continue
 m=ob.data;normals=[None]*len(m.loops)
 for f in m.polygons:
  f.use_smooth=abs(f.normal.z)<.1
  for li in f.loop_indices:
   p=m.vertices[m.loops[li].vertex_index].co;i=min(range(len(path)),key=lambda i:(p.x-path[i][0])**2+(p.y-path[i][1])**2);t=Vector(path[min(i+1,180)])-Vector(path[max(i-1,0)]);t.normalize();n=Vector((t.y,-t.x,0));side=abs(f.normal.dot(n))>.9
   normals[li]=tuple(n*(1 if f.normal.dot(n)>0 else -1))if side else tuple(f.normal)
 m.normals_split_custom_set(normals)
bpy.context.scene['glass_surface_refinement']='True concentric bent-glass thickness and analytic cylindrical corner normals; lower panels share full-path tangents. Physical transmission/IOR retained.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Analytic bent glass applied',count,'upper panels')
