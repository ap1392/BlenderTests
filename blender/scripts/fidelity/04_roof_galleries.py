exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Roof oak blade','Oculus plaster reveal','Skylight glazing','Atrium roof substrate')) or 'gallery oak blade' in o.name or 'acoustic ceiling' in o.name or 'office partition' in o.name or 'closed office door' in o.name or o.name.startswith('Door pull'))
C='Ceiling'
# Photo-supported rounded triangular lower mouths and offset tapered upper apertures.
holes=[]
for x,y,rx,ry,rot in [(-12,3.3,3.7,3.6,.3),(0,4,5.1,5.0,-.25),(12,8,3.2,3.05,.8)]:
 pts=[]
 for j in range(120):
  a=j*2*pi/120;r=1+.12*cos(3*a);u=rx*r*cos(a);v=ry*r*sin(a);pts.append((x+u*cos(rot)-v*sin(rot),y+u*sin(rot)+v*cos(rot)))
 holes.append(pts)
roofOutline=north+south[::-1]
roof=poly('Corrected atrium roof dark substrate',roofOutline,ROOF+.03,.3,black,False)
for idx,path in enumerate(holes):
 cut=poly('Temporary skylight cutting volume',path,ROOF+3,6,white,False)
 mod=roof.modifiers.new('Rounded triangular aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.context.view_layer.objects.active=roof;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 cx=sum(p[0]for p in path)/len(path);cy=sum(p[1]for p in path)/len(path)
 upper=[(cx+(x-cx)*.67-.3,cy+(y-cy)*.67+.6)for x,y in path]
 verts=[(x,y,ROOF-.58)for x,y in path]+[(x,y,ROOF+1.65+.07*(y-cy))for x,y in upper]
 N=len(path);ob=mesh(f'Skylight {idx+1} deep tapered white reveal',verts,[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],white);finish(ob,True)
 ribbon('Skylight smooth lower lip',path+[path[0]],[ROOF-.62]*(N+1),.10,.07,white,False)
 ob=poly('Skylight upper glass',upper,ROOF+1.68,.025,glass,False)
 # Frame traces upper opening; simple verified clear sky beyond.
 curve_tube('Skylight upper perimeter frame',[(x,y,ROOF+1.70)for x,y in upper+[upper[0]]],.035,white)
# Line-polygon intersection clips each straight blade exactly rather than jagged 0.2m raster ends.
def cross_intervals(x,pts):
 vals=[]
 for a,b in zip(pts,pts[1:]+pts[:1]):
  if (a[0]<=x<b[0])or(b[0]<=x<a[0]):vals.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
 vals.sort();return [(vals[i],vals[i+1])for i in range(0,len(vals)-1,2)]
def subtract(intervals,cuts):
 for ca,cb in cuts:
  out=[]
  for a,b in intervals:
   if cb<=a or ca>=b:out.append((a,b))
   else:
    if ca>a:out.append((a,ca))
    if cb<b:out.append((cb,b))
  intervals=out
 return intervals
for i in range(228):
 x=-24+i*.21;intervals=cross_intervals(x,roofOutline)
 for h in holes:intervals=subtract(intervals,cross_intervals(x,h))
 for a,b in intervals:
  if b-a>.03:box('Straight roof oak blade',(x,(a+b)/2,ROOF-.41),(.038,b-a,.21),wood)
# Parallel slats in each coherent balcony field; concealed services above.
for lev,z in enumerate(FLOORS[1:],2):
 outline=south+offset(south,3.4)[::-1]
 for i in range(221):
  x=-22+i*.21
  for a,b in cross_intervals(x,outline):
   if b-a>.06:box(f'L{lev} parallel gallery oak blade',(x,(a+b)/2,z+H-.46),(.038,b-a,.23),wood)
 strip(f'L{lev} high gallery acoustic backing',south,3.4,z+H-.09,.04,black,False)
 # Thin support rails above blades, fixed-direction black services remain visible through gaps.
 for y in [-9,-6,-3,0,3,6]:
  ranges=cross_intervals(y,[(p[1],p[0])for p in outline])
  for a,b in ranges:box('Ceiling dark carrier rail',((a+b)/2,y,z+H-.26),(b-a,.025,.025),dark)
# Public office fronts: glass, pale wood closed leaves, dark gray headers and frames.
C='Rooms';back=path_resample(offset(south,3.32),45);gray=bpy.data.materials.get('Office charcoal paint')or mat('Office charcoal paint',(.24,.25,.25),.8)
for lev,z in enumerate(FLOORS[1:],2):
 for i in range(len(back)-1):
  p,q=back[i:i+2]
  if i%4==1:ribbon('Closed oak office leaf',[p,q],[z,z],2.72,.075,wood)
  else:panel_glass('Office glazed public frontage',[p,q],z+.05,z+2.72)
  beam('Office silver vertical frame',(*p,z),(*p,z+2.76),.020,metal)
 ribbon('Office continuous gray header',back,[z+2.76]*len(back),H-2.76,.20,gray)
 # Bound unknown office depth with closed shallow walls; visible mullions are real frontage.
 rear=offset(back,2.8);ribbon('Office interior limited closure',rear,[z]*len(rear),3.0,.18,white)
# Documented social hub with rounded kitchenette opening, cabinet fronts and peninsula.
for lev,z in enumerate(FLOORS[1:],2):
 C='Architecture';hub=[(-7,-6),(-1,-3.8),(4,-3),(4,-10),(-7,-10)]
 poly(f'L{lev} social hub extension',hub,z,.42,white);poly(f'L{lev} social hub carpet',hub,z+.016,.016,carpet)
 # Rounded alcove face located behind public gallery, keeps unknown office rooms closed.
 C='Rooms';curve=smooth([(-.8,-8.4),(-.4,-9),(1.3,-9.6),(3.1,-9.6)],10)
 ribbon('Kitchenette curved gray upper surround',curve,[z+2.8]*len(curve),H-2.8,.30,gray)
 ribbon('Kitchenette pale recessed back',offset(curve,.4),[z]*len(curve),2.82,.18,white)
 ribbon('Kitchenette white cove underside',curve,[z+2.77]*len(curve),.07,1.05,white)
 C='Furniture';oak=bpy.data.materials['Light rift cut white oak'];cabmat=bpy.data.materials.get('Warm gray kitchen cabinets')or mat('Warm gray kitchen cabinets',(.41,.42,.40),.42)
 for x in [.2,.85,1.5,2.15,2.8]:
  box('Kitchenette base cabinet',(x,-9.03,z+.46),(.63,.64,.9),cabmat)
  for h in [.21,.44,.66]:
   box('Kitchenette horizontal drawer reveal',(x,-8.701,z+h),(.59,.005,.009),dark)
   beam('Kitchenette drawer pull',(x-.16,-8.68,z+h+.09),(x+.16,-8.68,z+h+.09),.009,metal)
 box('Kitchenette pale counter',(1.5,-9.03,z+.94),(3.30,.71,.04),white,False,.015)
 # Small visible sink and tap, no unsupported kitchen appliances.
 box('Kitchenette brushed sink bowl',(2.38,-8.98,z+.963),(.45,.37,.008),metal,False,.055)
 curve_tube('Kitchenette curved tap',[(2.5,-9.12,z+.98),(2.5,-9.12,z+1.2),(2.5,-8.98,z+1.27),(2.5,-8.90,z+1.2)],.013,metal)
 bar=smooth([(-.8,-7.85),(-.7,-7.32),(.1,-7.10),(1.3,-7.1),(1.7,-7.4)],10)
 ribbon('Kitchenette rounded white peninsula',bar,[z+.09]*len(bar),1.02,.15,white)
 strip('Kitchenette oak bar top',bar,.66,z+1.14,.045,oak)
 for x in [-.35,.30,.95]:
  box('Kitchenette pale oak stool seat',(x,-6.85,z+.79),(.41,.40,.04),oak,False,.025)
  for dx in [-.16,.16]:
   for dy in [-.15,.15]:box('Kitchenette stool oak leg',(x+dx,-6.85+dy,z+.39),(.04,.04,.78),oak)
 C='Ceiling'
 for x in [i*.21-7 for i in range(53)]:box('Social alcove parallel oak blade',(x,-8.7,z+H-.46),(.038,2.4,.23),wood)
# Wood-blade ceiling under laboratory wing, documented in ground photos.
C='Ceiling';under=north+offset(north,-7)[::-1]
for i in range(220):
 x=-22+i*.21
 for a,b in cross_intervals(x,under):box('Undercroft oak blade',(x,(a+b)/2,H-.89),(.038,b-a,.20),wood)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Roof, parallel ceilings, public fronts and social hubs saved')
