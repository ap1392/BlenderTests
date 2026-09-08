exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
if not bpy.data.materials.get('Concrete procedural diagnostic before bitmap'):
 old=concrete.copy();old.name='Concrete procedural diagnostic before bitmap'
nt=concrete.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.83;nt.links.new(bs.outputs[0],out.inputs['Surface'])
co=nt.nodes.new('ShaderNodeTexCoord');sc=nt.nodes.new('ShaderNodeVectorMath');sc.operation='MULTIPLY';sc.inputs[1].default_value=(1/4.6,1/1.45,1);nt.links.new(co.outputs['UV'],sc.inputs[0])
im=nt.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(ROOT/'blender/assets/textures/isec_board_formed_concrete_reconstruction_v1.png'),check_existing=True);im.image.pack();im.extension='REPEAT';nt.links.new(sc.outputs[0],im.inputs['Vector']);nt.links.new(im.outputs['Color'],bs.inputs['Base Color'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.0012;nt.links.new(im.outputs['Color'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
concrete['texture_provenance']='AI-generated texture reconstruction using Wausau2 concrete as visual material reference; not a recovered site photograph, scan or manufacturer map. Ten visible rows mapped to1.45m height.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
