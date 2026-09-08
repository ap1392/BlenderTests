exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Source REF03 has fine, restrained diamond quilting, not coarse puffed cells.
original = next(o for o in bpy.data.objects if 'Magenta social bucket shell' in o.name)
old = original.data
N, M = 288, 128
verts = []
for j in range(M + 1):
    t = j / M
    for i in range(N + 1):
        u = i / N
        a = -.2 + u * (pi + .4)
        padding = .0008 * sin(pi * ((u * 18 + t * 10) % 1)) ** 2 * sin(pi * ((u * 18 - t * 10) % 1)) ** 2
        r = .33 + .045 * t + padding
        verts.append((r * cos(a), (.27 + .025 * t + padding) * sin(a), .46 + t * (.22 + .16 * max(0, sin(a)))))
faces = [(j * (N + 1) + i, j * (N + 1) + i + 1, (j + 1) * (N + 1) + i + 1, (j + 1) * (N + 1) + i) for j in range(M) for i in range(N)]
ob = mesh('Fine quilted social chair template', verts, faces, pink)
finish(ob, True)
new = ob.data
count = 0
for item in bpy.data.objects:
    if item.data == old:
        item.data = new
        count += 1
bpy.data.objects.remove(ob, do_unlink=True)
bpy.context.scene['social_quilt_v50'] = 'Reduced coarse 3.5 mm padding to restrained 0.8 mm relief and doubled diamond frequency, matching the finer upholstered surface in REF03; dimensions remain approximate.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'blender/ISEC_Master.blend'))
print('Refined shared upholstery meshes:', count)
