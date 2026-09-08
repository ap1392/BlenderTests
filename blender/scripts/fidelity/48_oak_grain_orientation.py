exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
ma=bpy.data.materials['Light rift cut white oak'];seen=set()
for ob in bpy.data.objects:
 if ob.type!='MESH'or ma not in list(ob.data.materials)or ob.data in seen:continue
 seen.add(ob.data);m=ob.data;uv=m.uv_layers.get('Oak metric face grain')or m.uv_layers.new(name='Oak metric face grain');dx=max(v.co.x for v in m.vertices)-min(v.co.x for v in m.vertices);dy=max(v.co.y for v in m.vertices)-min(v.co.y for v in m.vertices)
 for f in m.polygons:
  normal=f.normal
  for li in f.loop_indices:
   p=m.vertices[m.loops[li].vertex_index].co
   if abs(normal.z)>.7:u,v=(p.x,p.y)if dx>dy else(p.y,p.x)
   elif abs(normal.x)>abs(normal.y):u,v=p.z,p.y
   else:u,v=p.z,p.x
   uv.data[li].uv=(u,v)
 m.uv_layers.active=uv
nt=ma.node_tree;co=next(n for n in nt.nodes if n.type=='TEX_COORD');mapping=next(n for n in nt.nodes if n.type=='VECT_MATH');mapping.inputs[1].default_value=(.8,55,1);nt.links.new(co.outputs['UV'],mapping.inputs[0])
ma['grain_orientation']='Metric face UV: long tabletop axis, vertical panel grain. Corrected from blanket world-Y grain.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Face-aligned oak grain on',len(seen),'shared meshes')
