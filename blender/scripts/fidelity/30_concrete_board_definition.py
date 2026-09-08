exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# The built wall shows strong horizontal board-to-board variation, not isotropic plaster.
nt=concrete.node_tree
brick=next(n for n in nt.nodes if n.type=='TEX_BRICK')
brick.inputs['Color1'].default_value=(.21,.22,.205,1)
brick.inputs['Color2'].default_value=(.41,.405,.365,1)
brick.inputs['Mortar'].default_value=(.22,.225,.205,1)
brick.inputs['Mortar Size'].default_value=.0013
# Retain metre-scaled UVs and thin form seams; subordinate the broad cloudy overlay.
for n in nt.nodes:
 if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY':
  n.inputs[0].default_value=.28 if n.inputs[2].is_linked and n.inputs[2].links[0].from_node.type=='VALTORGB' else .22
bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
bs.inputs['Roughness'].default_value=.83
bpy.context.scene['concrete_finish_evidence']='Wausau lower-stair and Payette hero photographs: horizontal form-board value changes; 145mm row and 4.6m length are photographic estimates.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Concrete board definition restored; broad mottling subordinated')
