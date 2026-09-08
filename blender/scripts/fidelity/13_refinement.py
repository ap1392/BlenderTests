exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# The pod kitchenette faces west toward its lounge, not north toward the atrium.
pivot=Vector((1,-8.5,0));rot=Matrix.Rotation(pi/2,4,'Z')
for o in bpy.data.objects:
 if o.name.startswith('Kitchenette') and o.type=='MESH':
  world=o.matrix_world.copy();inv=world.inverted()
  for v in o.data.vertices:
   p=world@v.co;v.co=inv@(pivot+rot@(p-pivot))
# Pink group is northwest of the lower approach in the published ground plan.
for o in bpy.data.objects:
 if o.name.startswith('Ground tall magenta tulip')or o.name.startswith('Tulip small white side table')or o.name.startswith('Tulip side table base'):o.location.x-=3.0
# Smooth the white structural skin at pitch-to-landing transitions; retain planar tread geometry.
for o in bpy.data.objects:
 if o.type!='MESH':continue
 step=4 if 'smooth spiral white stringer'in o.name else 2 if 'continuous stair soffit'in o.name else 0
 if not step:continue
 count=len(o.data.vertices)//step;zz=[o.data.vertices[i*step].co.z for i in range(count)]
 for i in range(1,count-1):
  radius=min(7,i,count-1-i);weights=[(radius+1-abs(j))for j in range(-radius,radius+1)];value=sum(zz[i+j]*w for j,w in zip(range(-radius,radius+1),weights))/sum(weights);delta=value-zz[i]
  for k in range(step):o.data.vertices[i*step+k].co.z+=delta
 finish(o,True)
# Muted formed concrete with longitudinal board grain, not alternating flat tiles.
nt=concrete.node_tree;bs=nt.nodes.get('Principled BSDF');brick=next(n for n in nt.nodes if n.type=='TEX_BRICK');brick.inputs['Color1'].default_value=(.16,.17,.16,1);brick.inputs['Color2'].default_value=(.26,.27,.25,1);brick.inputs['Mortar'].default_value=(.13,.14,.13,1)
coord=nt.nodes.new('ShaderNodeTexCoord');scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(.7,1.0,95);nt.links.new(coord.outputs['Object'],scale.inputs[0]);grain=nt.nodes.new('ShaderNodeTexNoise');grain.inputs['Scale'].default_value=2.5;grain.inputs['Detail'].default_value=3;nt.links.new(scale.outputs[0],grain.inputs['Vector']);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.20;nt.links.new(brick.outputs['Color'],mix.inputs[1]);nt.links.new(grain.outputs['Fac'],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
# Fill only documented public entrance/elevator fronts, keeping doors closed.
C='Rooms';steel=bpy.data.materials.get('Elevator brushed metal')or mat('Elevator brushed metal',(.32,.35,.36),.31,.8)
# Plan L1 elevator bank to southeast of the lower staircase, visible on the left of Wausau2.
for x in [3.0,5.0]:
 y=-6.1;box('Elevator closed brushed double leaves',(x,y,1.14),(1.55,.07,2.28),steel)
 box('Elevator central leaf joint',(x,y-.038,1.14),(.010,.002,2.25),dark)
 box('Elevator white lintel',(x,y,2.43),(1.83,.22,.22),white)
 for dx in [-.9,.9]:box('Elevator white jamb',(x+dx,y,1.2),(.14,.22,2.4),white)
 box('Elevator indicator dark face',(x,y-.13,2.61),(.21,.035,.12),dark)
 box('Elevator blue indicator',(x,y-.151,2.62),(.035,.006,.032),blue)
box('Elevator foyer gray backing',(4,-6.28,1.65),(5.5,.18,3.3),bpy.data.materials['Office charcoal paint'])
# Very distant ground replaces the accidental black horizon through glazed exits.
C='Exterior';box('Extended immediate exterior daylight ground',(0,0,-.7),(2400,2400,.3),bpy.data.materials['Exterior paving'])
# Camera adjustments tied to reference comparison, no hidden architecture.
def camera(name,loc,target,lens,shift=0):
 o=bpy.data.objects[name];o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.shift_y=shift
camera('REF03_Social_hub',(-6.4,-12.2,2*H+1.6),(1,-2,2*H+1.6),23,.025)
camera('REF05_Lower_stair',(9.8,9.0,1.55),(3.6,.6,2.8),30)
# Tables/seat shells should have soft continuous edge shading, not rectangular foam blocks.
for o in bpy.data.objects:
 if o.type=='MESH'and ('seat cushion'in o.name.lower()or'chair seat'in o.name.lower()):
  for mod in o.modifiers:
   if mod.type=='BEVEL':mod.segments=5
# Keep labels explicit: this is a reference-constrained reconstruction with residual uncertainty.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Pod orientation, concrete grain, stair skin and lower-front context refined')
