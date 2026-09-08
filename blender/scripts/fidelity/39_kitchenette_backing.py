exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Kitchenette pale recessed back','Kitchenette plan diagonal closed wall','Kitchenette canopy closed return')))
C='Rooms';gray=bpy.data.materials['Office charcoal paint']
for z in FLOORS[1:]:
 # Complete the real diagonal office-bank partition behind the sink and mural.
 path=[(1.06,-5.565),(3.06,-9.165)];finish(ribbon('Kitchenette plan diagonal closed wall',path,[z,z],H,.12,gray),True)
 # Close the upper enclosure at its sides, avoiding an unsupported floating hood edge.
 path=[(1,-5.6),(3,-9.2),(2.2,-10),(-.5,-10)];finish(ribbon('Kitchenette canopy closed return',path,[z+2.8]*4,H-2.8,.18,gray),True)
bpy.data.objects['REF03_Social_hub'].location=(-6.8,-12.75,10.439);bpy.data.objects['REF03_Social_hub'].data.shift_x=-.055;bpy.data.objects['REF03_Social_hub'].data.shift_y=.155
# Retain the best-supported hero viewpoint; all alternate cameras are diagnostic only.
remove_where(lambda o:o.type=='CAMERA'and o.name.startswith(('TEST01_','TEST03_')))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
