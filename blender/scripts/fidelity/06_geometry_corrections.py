exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:COL['Staircase'] in o.users_collection and (o.name.startswith(('L2-','L3-','L4-','L5-','Stair recessed traction','Radial stair glass','Circular glass clamp','Inset stainless helical','Concealed warm stair','Stair soffit panel')) or 'continuous stair soffit'in o.name or 'smooth spiral white stringer'in o.name))
exec(compile((ROOT/'blender/scripts/fidelity/01_height_stair.py').read_text(),'01_height_stair.py','exec'))
# Independent multi-view correction: J-lines in L1 are NOT the concrete auditorium wall.
remove_where(lambda o:o.name.startswith(('Traced J concrete enclosure wall','Concrete wall above wood-lined recess','Closed wood-lined recess wall','Auditorium documented north and east boundary')))
C='Atrium';aud=smooth(P([(678,450),(705,453),(730,467),(748,489),(759,518),(762,554),(757,580),(745,604)]),12)
finish(ribbon('Auditorium board formed concrete east curve',aud,[0]*len(aud),H+.90,.28,concrete),True)
# Above-door curved concrete return near the elevator foyer, visible underneath the upper flight.
C='Rooms';ribbon('Auditorium high concrete return',smooth(P([(745,604),(728,618),(707,625)]),10),[2.55]*21,H+.9-2.55,.28,concrete)
# Remove the hub extension that was projected into open atrium by an inaccurate generic polygon.
remove_where(lambda o:'social hub extension'in o.name or 'social hub carpet'in o.name)
# Extend only behind the traced south gallery edge, retaining the true void.
for lev,z in enumerate(FLOORS[1:],2):
 C='Architecture';hub=[(-7.0,-7.9),(-2.0,-5.2),(3.6,-2.9),(3.6,-10.0),(-7,-10)]
 # part of hub at x>1 is private pod: public visible alcove ends behind main gallery
 poly(f'L{lev} bounded social alcove floor',hub,z,.42,white);poly(f'L{lev} bounded social alcove carpet',hub,z+.017,.017,carpet)
# Reference camera corrections from the first twelve-way review.
def camera(name,loc,target,lens=None,shift=None):
 ob=bpy.data.objects[name];ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
 if lens is not None:ob.data.lens=lens
 if shift is not None:ob.data.shift_y=shift
# Original far registration had no near occluding slab. Keep camera at the front of the real bridge.
p=json.loads((ROOT/'references/fidelity/calibration/hero_initial_fit.json').read_text())['parameters']
camera('REF01_Payette_atrium',(p[0],p[1],H+1.5),(p[0]-math.cos(p[3]),p[1]+math.sin(p[3]),H+1.5),p[4]/1149*36,(p[5]-450)/1149)
camera('REF02_Reverse_soffit',(-3.4,-2.5,2*H+1.65),(15,10.0,H+2.1),22,0)
camera('REF03_Social_hub',(-5.8,-9.4,2*H+1.58),(.7,2.5,2*H+1.58),23,.025)
camera('REF04_Writeup',(-14,10.5,H+1.6),(18,14.5,H+1.6),20,0)
camera('REF05_Lower_stair',(10.7,10.7,1.55),(3.9,.7,2.3),32,0)
camera('REF07_Stair_elevation',(10.8,3.5,2*H+1.65),(0,-.5,2*H+2.9),37,0)
camera('REF08_Stair_overhead',(5,-6,4*H+2.8),(0,0,2*H+1),27,0)
camera('REF10_Glass_elevation',(9,-1,3*H+.8),(9,11,3*H+.8),28,0)
camera('REF11_End_bridge',(13.0,4.0,2*H+1.6),(20.8,11,2*H+1.9),21,0)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Handedness, auditorium identity and camera corrections saved')
