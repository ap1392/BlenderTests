exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Source: Payette social-hub photograph. The circular housings hang below the
# blades; their tops must not intersect the newly corrected ceiling field.
changed = []
for ob in bpy.data.objects:
    if ob.get('fixture_clearance_v49'):
        continue
    if ob.name.startswith(('Social pod varied drum', 'Social pod drum downlight')):
        dz = -.13
    elif ob.name.startswith(('Lobby drum housing', 'Lobby drum diffuser', 'Lobby drum illumination')):
        dz = -.16
    else:
        continue
    ob.location.z += dz
    ob['fixture_clearance_v49'] = True
    changed.append(ob.name)
C = 'Lighting'
for ob in list(bpy.data.objects):
    if not ob.name.startswith(('Social pod varied drum housing', 'Lobby drum housing')):
        continue
    vertices = [ob.matrix_world @ v.co for v in ob.data.vertices]
    top = max(v.z for v in vertices)
    p = sum(vertices, Vector()) / len(vertices)
    ceiling = round((top + .71) / H) * H
    for dx in [-.13, .13]:
        beam('Drum fine suspension cable', (p.x + dx, p.y, top), (p.x + dx, p.y, ceiling - .425), .002, metal)
bpy.context.scene['fixture_clearance_v49'] = 'Circular gallery fixtures lowered to leave approximately 70 mm below the oak blade bottoms, based on the Payette social-hub photograph; thin suspension wires added.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'blender/ISEC_Master.blend'))
print('Corrected fixture clearance for', len(changed), 'housing, diffuser and light objects')
