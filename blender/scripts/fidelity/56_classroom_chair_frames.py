exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# The shallow classroom rows already existed, but their back pads and seats
# lacked visible support. Complete only a restrained generic steel frame; the
# exact chair product was not established from the distant photographed view.
C='Furniture';count=0
for seat in list(bpy.data.objects):
 if not seat.name.startswith('L1 documented classroom teal seat') or seat.get('frame_complete_v56'):continue
 center=seat.location.copy();v=Vector((cos(seat.rotation_euler.z),sin(seat.rotation_euler.z),0));n=Vector((-v.y,v.x,0))
 for side in [-1,1]:
  front=center+v*(side*.16)-n*.13;rear=center+v*(side*.16)+n*.14
  beam('Classroom chair front steel leg',(front.x,front.y,.445),(front.x+v.x*side*.03-n.x*.025,front.y+v.y*side*.03-n.y*.025,.035),.0095,metal)
  beam('Classroom chair connected rear leg and back upright',(rear.x+v.x*side*.025,rear.y+v.y*side*.025,.035),(rear.x+n.x*.04,rear.y+n.y*.04,.925),.0095,metal)
  beam('Classroom chair side seat support',front,rear,.009,metal)
 seat['frame_complete_v56']=True;count+=1
bpy.context.scene['classroom_frames_v56']='Completed previously unsupported-looking classroom seat/back pads with restrained connected steel legs and back uprights. Generic frame topology is inferred; no claim of manufacturer CAD.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Completed steel frames on',count,'classroom chairs')
