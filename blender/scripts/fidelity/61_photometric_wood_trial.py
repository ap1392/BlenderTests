import bpy
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
original=bpy.data.materials['Light rift cut white oak']
trial=bpy.data.materials.new('Photometric pale hardwood candidate');trial.use_nodes=True
nt=trial.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');nt.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
bs.inputs['Coat Weight'].default_value=.10;bs.inputs['Coat Roughness'].default_value=.32
co=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(co.outputs['UV'],sep.inputs[0]);combine=nt.nodes.new('ShaderNodeCombineXYZ')
# Existing metric UV U follows long tabletop axes / vertical panel grain.
# The photographed texture grain is vertical, so swap U and V.
nt.links.new(sep.outputs['Y'],combine.inputs['X']);nt.links.new(sep.outputs['X'],combine.inputs['Y']);scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=2.5;nt.links.new(combine.outputs[0],scale.inputs[0])
base=root/'references/fidelity/material_candidates/Wood056'
def texture(kind,noncolor=False):
 im=bpy.data.images.load(str(base/f'Wood056_1K-JPG_{kind}.jpg'),check_existing=True)
 if noncolor:im.colorspace_settings.name='Non-Color'
 node=nt.nodes.new('ShaderNodeTexImage');node.image=im;node.extension='REPEAT';nt.links.new(scale.outputs[0],node.inputs['Vector']);return node
color=texture('Color');lum=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(color.outputs['Color'],lum.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.08;ramp.color_ramp.elements[0].color=(.38,.29,.18,1)
ramp.color_ramp.elements[1].position=.35;ramp.color_ramp.elements[1].color=(.61,.50,.34,1)
nt.links.new(lum.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
rough=texture('Roughness',True);mr=nt.nodes.new('ShaderNodeMapRange');mr.inputs['To Min'].default_value=.36;mr.inputs['To Max'].default_value=.52;nt.links.new(rough.outputs['Color'],mr.inputs['Value']);nt.links.new(mr.outputs[0],bs.inputs['Roughness'])
normal=texture('NormalGL',True);nm=nt.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.12;nt.links.new(normal.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs[0],bs.inputs['Normal'])
trial['source']='https://ambientcg.com/view?id=Wood056';trial['license']='CC0';trial['physical_tile_m']=.4;trial['provenance']='Independent photometric stereo wood sample, species unverified; pale color calibrated to ISEC photographs. Not an ISEC scan.'
seen=set();changed=0
for ob in bpy.data.objects:
 if ob.type!='MESH'or ob.data in seen:continue
 seen.add(ob.data)
 for i,ma in enumerate(ob.data.materials):
  if ma==original:ob.data.materials[i]=trial;changed+=1
print('Photometric wood trial assigned to',changed,'shared mesh material slots; master not saved')
