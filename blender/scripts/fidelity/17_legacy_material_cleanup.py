exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Obsolete blockout closures were hidden behind/above the later, documented frontage.
# They interrupted long laboratory islands and masked the exposed ceiling channels.
remove_where(lambda o:any(o.name==f'L{k} '+n for k in range(2,7)for n in ['rear laboratory boundary','lab ceiling']))
# Map concrete boards by arclength in metres, so form grain follows the curved auditorium.
for ob in bpy.data.objects:
 if ob.type!='MESH' or concrete not in list(ob.data.materials):continue
 if len(ob.data.vertices)%4:continue
 count=len(ob.data.vertices)//4;distance=[0.0]
 for i in range(1,count):distance.append(distance[-1]+(ob.data.vertices[i*4].co-ob.data.vertices[(i-1)*4].co).length)
 uv=ob.data.uv_layers.get('Concrete formwork metric')or ob.data.uv_layers.new(name='Concrete formwork metric')
 for loop in ob.data.loops:
  v=ob.data.vertices[loop.vertex_index];uv.data[loop.index].uv=(distance[loop.vertex_index//4],v.co.z)
 ob.data.uv_layers.active=uv
nt=concrete.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.81;nt.links.new(bs.outputs[0],out.inputs['Surface'])
coord=nt.nodes.new('ShaderNodeTexCoord');brick=nt.nodes.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=4.6;brick.inputs['Row Height'].default_value=.145;brick.inputs['Mortar Size'].default_value=.0008;brick.inputs['Mortar Smooth'].default_value=.001;brick.offset=.37;brick.offset_frequency=3
brick.inputs['Color1'].default_value=(.30,.31,.295,1);brick.inputs['Color2'].default_value=(.33,.335,.31,1);brick.inputs['Mortar'].default_value=(.275,.28,.26,1);nt.links.new(coord.outputs['UV'],brick.inputs['Vector'])
scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(.8,145,1);nt.links.new(coord.outputs['UV'],scale.inputs[0]);grain=nt.nodes.new('ShaderNodeTexNoise');grain.inputs['Scale'].default_value=1;grain.inputs['Detail'].default_value=3;nt.links.new(scale.outputs[0],grain.inputs['Vector'])
mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.10;nt.links.new(brick.outputs['Color'],mix.inputs[1]);nt.links.new(grain.outputs['Fac'],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.0007;nt.links.new(grain.outputs['Fac'],bump.inputs['Height'])
seam=nt.nodes.new('ShaderNodeBump');seam.inputs['Strength'].default_value=.25;seam.inputs['Distance'].default_value=.0012;nt.links.new(brick.outputs['Fac'],seam.inputs['Height']);nt.links.new(bump.outputs[0],seam.inputs['Normal']);nt.links.new(seam.outputs[0],bs.inputs['Normal'])
# Floor colour inlay is effectively flush, not a separate raised strip.
for ob in bpy.data.objects:
 if ob.name.startswith('Curving terrazzo tonal band'):
  for v in ob.data.vertices:v.co.z=.0005 if v.co.z>.003 else -.0002
  finish(ob)
# Frit lies on the public-facing glass surface, with 1.5mm separation to avoid coincident faces.
for ob in bpy.data.objects:
 if ob.name.startswith('Horizontal ceramic frit line'):
  for i in range(0,len(ob.data.vertices),4):
   p=ob.data.vertices[i].co;q=ob.data.vertices[i+1].co;d=q-p;d.z=0
   if d.length:
    d.normalize()
    for j in range(4):ob.data.vertices[i+j].co+=d*.002
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Obsolete lab closures removed; metre UV concrete and flush inlay corrected')
