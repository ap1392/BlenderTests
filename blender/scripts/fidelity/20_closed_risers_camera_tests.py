exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Thin prototype tread plates left 77–82mm OPEN gaps between risers. The real E31 stair
# is closed-riser terrazzo. Make the tread body reach the preceding tread elevation.
terrazzo=bpy.data.materials.get('Wausau E31 light terrazzo')or floor.copy();terrazzo.name='Wausau E31 light terrazzo'
for node in terrazzo.node_tree.nodes:
 if node.type=='VALTORGB':node.color_ramp.elements[0].color=(.62,.62,.585,1);node.color_ramp.elements[1].color=(.79,.78,.73,1)
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 if 'terrazzo tread'in ob.name or ob.name.startswith('Fidelity lower stair tread'):rise=H/30
 elif ob.name.startswith('Corrected broad stair tread'):rise=H/28
 else:continue
 top=max(v.co.z for v in ob.data.vertices);bottom=min(v.co.z for v in ob.data.vertices)
 for v in ob.data.vertices:
  if abs(v.co.z-bottom)<.0001:v.co.z=top-rise-.006
 ob.data.materials.clear();ob.data.materials.append(terrazzo);finish(ob)
# Four low-cost perspective tests at actual L2 eye height, tied to the helix geometry.
base=bpy.data.objects['REF02_Reverse_soffit'];remove_where(lambda o:o.name.startswith('TEST02_'))
for idx,(x,y)in enumerate([(1,-3.8),(.6,-3.8),(1.4,-4.2),(0,-4.4)]):
 data=base.data.copy();ob=bpy.data.objects.new('TEST02_'+str(idx+1),data);COL['Cameras'].objects.link(ob);ob.location=(x,y,H+1.6);ob.rotation_euler=(Vector((18,10,H+1))-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=22;ob.data.shift_y=0;ob['render_width']=1098;ob['render_height']=900
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Closed riser geometry and L2 camera experiments saved')
