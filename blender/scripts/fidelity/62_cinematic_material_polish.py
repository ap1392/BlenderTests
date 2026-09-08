"""Bounded material polish; preserves all architectural positions and camera registration."""
import bpy
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/backups/ISEC_post60_before_cinematic.blend'),copy=True)

def principled(name):
    m=bpy.data.materials[name]
    return m,m.node_tree,next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')

# The old common white shader made plaster, enamel and fixtures equally glossy.
m,nt,bs=principled('Warm white painted steel and plaster')
enamel=m.copy();enamel.name='Cinematic satin white architectural enamel'
eb=next(n for n in enamel.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
eb.inputs['Base Color'].default_value=(.79,.80,.79,1)
eb.inputs['Roughness'].default_value=.28
bs.inputs['Roughness'].default_value=.53
for ob in bpy.data.objects:
    if ob.type!='MESH':continue
    if any(word in ob.name.lower() for word in ['stringer','stair skin','stair soffit','ribbon','luminaire housing','drum housing','pendant housing']):
        for slot in ob.material_slots:
            if slot.material==m:slot.material=enamel

# Preserve physically refractive glass. Lower the small accumulated color tint;
# retain paired surfaces, IOR and geometric normals rather than alpha shortcuts.
m,nt,bs=principled('Clear architectural glazing')
bs.inputs['Base Color'].default_value=(.992,.998,1,1)
bs.inputs['Roughness'].default_value=.009
m['cinematic_polish']='Near-neutral clear glass; actual paired surfaces retained. Optical values remain estimates.'

# Narrow the broad, synthetic veneer bands, then mix in a finer irregular pore scale.
m,nt,bs=principled('Light rift cut white oak')
mapping=next(n for n in nt.nodes if n.type=='VECT_MATH')
mapping.inputs[1].default_value=(1.1,180,1)
noise=next(n for n in nt.nodes if n.type=='TEX_NOISE')
noise.inputs['Detail'].default_value=3.5
ramp=next(n for n in nt.nodes if n.type=='VALTORGB')
ramp.color_ramp.elements[0].color=(.40,.285,.16,1)
ramp.color_ramp.elements[1].color=(.61,.465,.285,1)
bump=next(n for n in nt.nodes if n.type=='BUMP')
bump.inputs['Strength'].default_value=.08
bump.inputs['Distance'].default_value=.0003
bs.inputs['Roughness'].default_value=.38
bs.inputs['Coat Weight'].default_value=.10
bs.inputs['Coat Roughness'].default_value=.35

# Carpet reads as fine commercial pile, not broad mottled concrete.
for name,lo,hi in [('Charcoal carpet',(.025,.032,.035,1),(.056,.064,.068,1)),
                   ('Write-up warm grey carpet',(.18,.16,.145,1),(.235,.211,.19,1))]:
    m,nt,bs=principled(name)
    ramp=next(n for n in nt.nodes if n.type=='VALTORGB')
    ramp.color_ramp.elements[0].color=lo;ramp.color_ramp.elements[1].color=hi
    bs.inputs['Sheen Weight'].default_value=.18
    bs.inputs['Specular IOR Level'].default_value=.28

# Smooth resin-bound aggregate has shallow relief and a distinct satin response.
for name in ['Pale grey terrazzo','Wausau E31 light terrazzo']:
    m,nt,bs=principled(name)
    bs.inputs['Roughness'].default_value=.25 if name.startswith('Pale') else .30
    bump=next(n for n in nt.nodes if n.type=='BUMP')
    bump.inputs['Distance'].default_value=.00018
    bump.inputs['Strength'].default_value=.08

# Fine concrete roughness variation does not change the reference board pattern.
m,nt,bs=principled('Board formed grey concrete')
coord=next(n for n in nt.nodes if n.type=='TEX_COORD')
noise=nt.nodes.new('ShaderNodeTexNoise');noise.name='Cinematic concrete fine pore roughness'
noise.inputs['Scale'].default_value=190;noise.inputs['Detail'].default_value=2
nt.links.new(coord.outputs['Object'],noise.inputs['Vector'])
rr=nt.nodes.new('ShaderNodeMapRange');rr.inputs['To Min'].default_value=.72;rr.inputs['To Max'].default_value=.88
nt.links.new(noise.outputs['Fac'],rr.inputs['Value']);nt.links.new(rr.outputs[0],bs.inputs['Roughness'])
for n in nt.nodes:
    if n.type=='BUMP':n.inputs['Distance'].default_value=.0007

# Keep the common sun/daylight solution; slightly strengthen skylight bounce.
world=bpy.context.scene.world
bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
bg.inputs['Strength'].default_value=.19
bpy.context.scene['cinematic_material_revision']='62 trial: reference-matched review pending'
print('Material trial62 applied without saving over master')
