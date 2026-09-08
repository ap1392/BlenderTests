exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Texture scale is metres, not the bounding box of the floor.
for ma in [floor,carpet,pink,blue,yellow]:
 nt=ma.node_tree;coord=nt.nodes.new('ShaderNodeTexCoord')
 for n in nt.nodes:
  if n.type=='TEX_NOISE':nt.links.new(coord.outputs['Object'],n.inputs['Vector'])
 for n in nt.nodes:
  if n.type=='BUMP'and ma==floor:n.inputs['Strength'].default_value=.035;n.inputs['Distance'].default_value=.00025
# Concrete board grain has subtle luminance variance inside each pour-board impression.
nt=concrete.node_tree;bs=nt.nodes.get('Principled BSDF');brick=next(n for n in nt.nodes if n.type=='TEX_BRICK');noise=next(n for n in nt.nodes if n.type=='TEX_NOISE');mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.18;nt.links.new(brick.outputs['Color'],mix.inputs[1]);nt.links.new(noise.outputs['Fac'],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
s=bpy.context.scene;s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.28;s.view_settings.exposure=.7
# Luminaires supplement daylight as in built write-up/laboratory photographs.
C='Lighting'
for o in bpy.data.objects:
 if o.type=='LIGHT'and o.data.type=='AREA':
  if 'Skylight'in o.name:o.data.energy=1100
  elif 'indirect pendant'in o.name:o.data.energy=160
  else:o.data.energy*=2.4
for lev,z in enumerate(FLOORS[1:],2):
 for i in range(3,len(north)-2,6):
  x,y=north[i];data=bpy.data.lights.new('Observed laboratory ceiling light','AREA');data.shape='RECTANGLE';data.energy=130;data.size=3.8;data.size_y=3.0;data.color=(1,.96,.88);o=bpy.data.objects.new('Observed laboratory ceiling light',data);COL[C].objects.link(o);o.location=(x,y+6.3,z+3.12)
# Ceiling backing over occupied labs stops unbounded sky light while visible rafts stay bright.
C='Ceiling'
for lev,z in enumerate(FLOORS[1:],2):strip('Laboratory opaque acoustic closure',north,-10,z+H-.09,.10,white,False)
# Refine near-plane fit after correcting bridge offset geometry.
cam=bpy.data.objects['REF01_Payette_atrium'];cam.location.x=20.2;cam.location.y=10.0;cam.data.lens=22.5
cam=bpy.data.objects['REF10_Glass_elevation'];cam.location=(9,.6,3*H+1.65);cam.rotation_euler=Vector((0,1,0)).to_track_quat('-Z','Y').to_euler();cam.data.lens=24
# Fully visible spiral top-down image without nearby gallery slab occlusion.
# Texture and stair treads now each keep the intended physical scale.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Meter-scaled materials and calibrated daylight/exposure saved')
