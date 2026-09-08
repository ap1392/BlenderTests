exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith('Kitchenette plan diagonal closed wall'))
C='Rooms'
for ob in list(bpy.data.objects):
 if not ob.name.startswith('Kitchenette reference-derived mural'):continue
 pp=[ob.matrix_world@v.co for v in ob.data.vertices];a=Vector(pp[0][:2]);b=Vector(pp[1][:2]);d=(b-a).normalized();n=Vector((d.y,-d.x));a=a-d*.18+n*.012;b=b+d*.18+n*.012;z=round((min(v.z for v in pp)-1.14)/H)*H
 finish(ribbon('Kitchenette plan diagonal closed wall',[tuple(a),tuple(b)],[z,z],H,.12,bpy.data.materials['Office charcoal paint']))
# One old drum overlaps the newly correctly placed canopy. Retain its fixture family,
# move it into the adjacent visible ceiling field with clear physical separation.
for ob in bpy.data.objects:
 if not ob.name.startswith(('Social pod varied drum','Social pod drum downlight'))or ob.get('canopy_clearance_v40'):continue
 p=ob.matrix_world@(sum((Vector(v)for v in ob.bound_box),Vector())/8)if ob.type=='MESH'else ob.location
 if abs(p.x+1.4)<.2 and abs(p.y+8.3)<.2:ob.location.x-=1.5;ob.location.y+=.2;ob['canopy_clearance_v40']=True
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
