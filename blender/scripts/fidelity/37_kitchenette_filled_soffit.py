exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Kitchenette white cove underside','Kitchenette filled recessed soffit')))
C='Rooms'
for ob in list(bpy.data.objects):
 if not ob.name.startswith('Kitchenette curved gray upper surround'):continue
 path=[tuple((ob.matrix_world@ob.data.vertices[i].co)[:2])for i in range(0,len(ob.data.vertices),4)]
 bottom=min((ob.matrix_world@v.co).z for v in ob.data.vertices)
 # Front curve to the known mural wall, filled rather than a thin edge strip.
 outline=path+[(2.5,path[-1][1]),(2.5,path[0][1])]
 pp=poly('Kitchenette filled recessed soffit',outline,bottom+.015,.08,white);finish(pp)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
