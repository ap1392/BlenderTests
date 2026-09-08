exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Backing must be below the structural slab underside to be visible between ceiling rafts.
for ob in bpy.data.objects:
 if ob.name.startswith('Laboratory opaque acoustic closure')and not ob.get('backing_clearance_corrected'):
  ob.location.z-=.35;ob['backing_clearance_corrected']=True
# Restrained irregular concrete tone within the measured-scale board impressions.
nt=concrete.node_tree;bs=nt.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket;co=next(n for n in nt.nodes if n.type=='TEX_COORD');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=7;noise.inputs['Detail'].default_value=3;nt.links.new(co.outputs['UV'],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=(.58,.60,.59,1);ramp.color_ramp.elements[1].position=.79;ramp.color_ramp.elements[1].color=(1.10,1.08,1.04,1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.55;nt.links.new(old,mix.inputs[1]);nt.links.new(ramp.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
# Source011's blue back is the near chair of the undercroft cluster; preserve chair scale.
oldcenter=Vector((10,14.5,0));newcenter=Vector((9.3,12.8,0));rotation=Matrix.Rotation(-2.37,4,'Z')
for ob in bpy.data.objects:
 if ob.location.z>.1 or not ob.name.startswith(('Petrol lounge','Pewter lounge','Ground cafe table')):continue
 if 9<ob.location.x<11 and 13.5<ob.location.y<15.5:
  ob.location=newcenter+rotation@(ob.location-oldcenter);ob.rotation_euler.z-=2.37
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Visible plenum backing, concrete surface variance and final photographed chair grouping saved')
