exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Peerless type linear pendant housing','Linear pendant warm diffuser','Linear pendant suspension')))
C='Lighting';line=path_resample(north,27)
for z in FLOORS[1:]:
 for i in range(1,25,3):
  p=Vector(offset(line,-2.0)[i]);box('Cross-corridor linear pendant housing',(*p,z+2.85),(.11,3.3,.085),white)
  box('Cross-corridor linear warm diffuser',(p.x,p.y,z+2.805),(.085,3.2,.012),em)
  for dy in [-1.2,1.2]:beam('Cross-corridor pendant suspension',(p.x,p.y+dy,z+2.9),(p.x,p.y+dy,z+3.24),.003,metal)
# Documented substantial bench service uprights and low mobile oak storage.
C='Furniture';worktop=bpy.data.materials['Warm white laboratory epoxy']
for ob in list(bpy.data.objects):
 if ob.name.startswith('Lab slim vertical service spine') and not ob.get('source_profile_v36'):
  vs=ob.data.vertices;cx=sum(v.co.x for v in vs)/len(vs);cy=sum(v.co.y for v in vs)/len(vs);base=round((min(v.co.z for v in vs)-.58)/H)*H
  for v in vs:
   v.co.x=cx+(v.co.x-cx)*2;v.co.y=cy+(v.co.y-cy)*2.5
   v.co.z=base+.04 if v.co.z<base+1.42 else base+2.32
  ob['source_profile_v36']=True;finish(ob)
  for zz in [1.11,1.53,1.94]:
   for side in [-1,1]:
    box('Visible service spine outlet plate',(cx+side*.057,cy,base+zz),(.009,.15,.065),white)
    for dy in [-.043,.043]:finish(beam('Service spine round outlet',(cx+side*.063,cy+dy,base+zz),(cx+side*.069,cy+dy,base+zz),.012,dark),True)
 if ob.name.startswith('Lab visible oak drawer pedestal') and not ob.get('drawer_detail_v36'):
  vs=ob.data.vertices;cx=sum(v.co.x for v in vs)/len(vs);cy=sum(v.co.y for v in vs)/len(vs);base=round((min(v.co.z for v in vs)-.05)/H)*H
  for h in [.28,.50,.70]:beam('Lab mobile drawer silver pull',(cx+.299,cy-.13,base+h-.08),(cx+.299,cy+.13,base+h-.08),.009,metal)
  for dx in [-.22,.22]:
   for dy in [-.20,.20]:finish(beam('Lab pedestal caster',(cx+dx-.025,cy+dy,base+.046),(cx+dx+.025,cy+dy,base+.046),.043,dark),True)
  ob['drawer_detail_v36']=True
# Less uniform horizontal concrete tone plus stronger longitudinal wood imprint.
nt=concrete.node_tree;br=next(n for n in nt.nodes if n.type=='TEX_BRICK');br.inputs['Color1'].default_value=(.245,.25,.23,1);br.inputs['Color2'].default_value=(.385,.38,.345,1)
grain=next(n for n in nt.nodes if n.type=='TEX_NOISE' and n.inputs['Scale'].default_value==1)
ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.name='Formwork fine grain contrast';ramp.color_ramp.elements[0].position=.28;ramp.color_ramp.elements[0].color=(.40,.40,.40,1);ramp.color_ramp.elements[1].position=.72;ramp.color_ramp.elements[1].color=(1.1,1.1,1.1,1);nt.links.new(grain.outputs['Fac'],ramp.inputs[0])
for n in nt.nodes:
 if n.type=='MIX_RGB' and n.inputs[2].is_linked and n.inputs[2].links[0].from_node==grain:
  nt.links.new(ramp.outputs[0],n.inputs[2]);n.inputs[0].default_value=.45
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
