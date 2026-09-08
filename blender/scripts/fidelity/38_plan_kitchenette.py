exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Published L4 plan grid: rear counter(1,-5.6) to(3,-9.2), oval island centred(-.45,-8.05).
old=Vector((1.77,-7.925,0));new=Vector((2,-7.4,0));rot=Matrix.Rotation(math.atan2(2,3.5),4,'Z')
backnames=('Kitchenette base cabinet','Kitchenette horizontal drawer reveal','Kitchenette drawer pull','Kitchenette pale counter','Kitchenette brushed sink bowl','Kitchenette pale recessed back','Kitchenette reference-derived mural')
for ob in bpy.data.objects:
 if ob.type=='MESH' and ob.name.startswith(backnames)and not ob.get('plan_bank_v38'):
  inv=ob.matrix_world.inverted()
  for v in ob.data.vertices:
   p=ob.matrix_world@v.co;d=p-old;d.y*=1.21;v.co=inv@(new+rot@d)
  ob['plan_bank_v38']=True;finish(ob)
# The original single curved front was not the freestanding oval drawn on the plan.
remove_where(lambda o:o.name.startswith(('Kitchenette rounded white peninsula','Kitchenette oak bar top','Kitchenette recessed dark plinth','Kitchenette curved gray upper surround','Kitchenette filled recessed soffit','Kitchenette curved tap','Kitchenette soffit recessed downlight','Kitchenette soffit warm downlight','Kitchenette plan oval','Kitchenette photo canopy','Kitchenette diagonal tap')))
# Move existing stools to the documented lounge side of the oval.
for ob in bpy.data.objects:
 if ob.type=='MESH'and ob.name.startswith(('Kitchenette pale oak stool','Kitchenette stool oak leg'))and not ob.get('plan_stool_v38'):
  for v in ob.data.vertices:v.co.x-=.80;v.co.y=-8.05+(v.co.y+9.2)*(0.8/.65)
  ob['plan_stool_v38']=True
C='Furniture';oak=bpy.data.materials['Light rift cut white oak']
def capsule(rx,straight,cx=-.45,cy=-8.05):
 pts=[]
 for j in range(33):
  a=j*pi/32;pts.append((cx+rx*cos(a),cy+straight/2+rx*sin(a)))
 for j in range(33):
  a=pi+j*pi/32;pts.append((cx+rx*cos(a),cy-straight/2+rx*sin(a)))
 return pts
for z in FLOORS[1:]:
 finish(poly('Kitchenette plan oval closed white body',capsule(.575,1.1),z+1.08,.95,white),True)
 finish(poly('Kitchenette plan oval dark toe recess',capsule(.53,1.02),z+.14,.105,dark),True)
 ob=poly('Kitchenette plan oval pale oak counter',capsule(.65,1.1),z+1.13,.05,oak);finish(ob,True)
 # Sink/counter objects remain bounded to the documented visible fixture.
 normal=Vector((-.868,-.496,0));p=Vector((1.6,-7.3,z+.97));pts=[tuple(p+Vector((0,0,h))+normal*d)for h,d in [(0,0),(.24,0),(.30,.10),(.25,.18)]];curve_tube('Kitchenette diagonal tap',pts,.013,metal)
 C='Rooms'
 front=smooth([(-.5,-10),(-1.35,-9.5),(-1.45,-8.2),(-1.2,-6.9),(-.25,-6.05),(1,-5.6)],10)
 outline=front+[(3,-9.2),(2.2,-10)]
 finish(ribbon('Kitchenette photo canopy gray curved face',front,[z+2.80]*len(front),H-2.8,.22,bpy.data.materials['Office charcoal paint']),True)
 finish(poly('Kitchenette photo canopy deep white soffit',outline,z+2.81,.08,white))
 C='Lighting'
 for x,y in [(-.75,-8.9),(-.7,-7.7),(.2,-6.55)]:
  finish(beam('Kitchenette photo canopy downlight optic',(x,y,z+2.725),(x,y,z+2.746),.048,em),True)
  d=bpy.data.lights.new('Kitchenette photo canopy warm downlight','AREA');d.energy=20;d.shape='DISK';d.size=.16;d.color=(1,.80,.60);ob=bpy.data.objects.new(d.name,d);COL[C].objects.link(ob);ob.location=(x,y,z+2.71)
 C='Furniture'
# Dark blue-gray social carpet; write-up retains its separate warmer material.
for n in carpet.node_tree.nodes:
 if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.011,.015,.018,1);n.color_ramp.elements[1].color=(.038,.048,.056,1)
# The backward camera is a viable physical position immediately inside the rear wall.
cam=bpy.data.objects['REF03_Social_hub'];cam.location=(-7.28,-13.41,10.439);cam.data.shift_x=-.025
bpy.context.scene['kitchenette_plan_evidence']='L4 published sink-counter diagonal and closed oval island grid verified. Island1.3x2.4m at(-.45,-8.05); repeated floor layout inferred; canopy curve photo-derived, not a reflected-ceiling plan.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
