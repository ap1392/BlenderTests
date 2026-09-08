# Runs in the build script namespace. Visible detail based on photo references.
# Smooth white helical soffits are key to the real stair silhouette.
C='Staircase'
for lev in range(1,5):
 z0=FLOORS[lev];aa=start;hh=z0;az=[(aa,hh)]
 for g in range(3):
  for j in range(10):aa+=math.radians(10.4);hh+=.14;az.append((aa,hh))
  aa+=math.radians(16);az.append((aa,hh))
 v=[]
 for i in range(len(az)-1):
  for j in range(5):
   t=j/5;a=az[i][0]*(1-t)+az[i+1][0]*t;z=az[i][1]*(1-t)+az[i+1][1]*t-.23
   v.extend([(ri*cos(a),ri*sin(a),z),(ro*cos(a),ro*sin(a),z)])
 a,z=az[-1];v.extend([(ri*cos(a),ri*sin(a),z-.23),(ro*cos(a),ro*sin(a),z-.23)])
 mesh(f'L{lev+1} smooth spiral soffit',v,[(i,i+1,i+3,i+2)for i in range(0,len(v)-2,2)],white)
# Oak slats: clip each strip against plan polygon and the three roof apertures.
C='Ceiling'
def inside(x,y,pts):
 b=False;j=len(pts)-1
 for i in range(len(pts)):
  xi,yi=pts[i];xj,yj=pts[j]
  if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi:b=not b
  j=i
 return b
holes=[(-12,3,4.1,3.2),(0,2,3.9,4.8),(12,8.2,3,2.9)]
for ix in range(210):
 x=-22+ix*.205;run=None
 for iy in range(141):
  y=-14+iy*.20;ok=inside(x,y,roofOutline) and not any(((x-a)/rx)**2+((y-b)/ry)**2<1.025 for a,b,rx,ry in holes)
  if ok and run is None:run=y
  if run is not None and (not ok or iy==140):
   box('Roof oak blade',(x,(run+y)/2,ROOF-.30),(.055,max(.1,y-run),.28),wood);run=None
# Gallery slats aligned across corridor, their outer ends follow the curved edge.
for lev,z in enumerate(FLOORS[1:],2):
 for i in range(len(south)-1):
  a,b=Vector(south[i]),Vector(south[i+1]);d=b-a;count=max(1,int(d.length/.20));d.normalize();normal=Vector((d.y,-d.x))
  for j in range(count):
   p=a.lerp(b,j/count);q=p+3.27*normal
   # narrow rectangular blade as beam with local angle
   delta=q-p;mid=(p+q)/2;ob=box(f'L{lev} gallery oak blade',(mid.x,mid.y,z+3.79),(3.27,.05,.24),wood);# baked coords currently centered: rotate mesh about center
   angle=math.atan2(delta.y,delta.x)
   for v in ob.data.vertices:
    vx,vy=v.co.x-mid.x,v.co.y-mid.y;v.co.x=mid.x+vx*cos(angle)-vy*sin(angle);v.co.y=mid.y+vx*sin(angle)+vy*cos(angle)
 # ceiling backing above blades
 strip(f'L{lev} acoustic ceiling',south,3.3,z+3.96,.06,black,False)
# Concrete board-form horizontal impressions.
C='Atrium'
for h in range(1,29):ribbon('Concrete board-form joint',core_path,[h*.14]*71,.012,.008,mat('Concrete joint '+str(h),(.27,.29,.28),.9),False)
# Round drum pendants in social hubs and bridge lobbies.
C='Lighting'
for lev,z in enumerate(FLOORS[1:],2):
 for x,y,r in [(-15,-2,.55),(-12,-4,.8),(-10,-6,.45),(7,-2,.55),(12,.5,.72),(18,3,.55),(-20,4,.6)]:
  beam(f'L{lev} pendant housing',(x,y,z+3.40),(x,y,z+3.61),r,white)
  beam(f'L{lev} pendant diffuser',(x,y,z+3.385),(x,y,z+3.40),r*.95,em)
  beam('Pendant suspension',(x,y,z+3.61),(x,y,z+3.91),.009,metal)
# Furniture meshes are reused through data-linked copies on subsequent chairs.
C='Furniture'
def ellipsoid(n,loc,sc,m):
 N=20;M=12;v=[]
 for j in range(M+1):
  a=-pi/2+j*pi/M
  for i in range(N):
   b=i*2*pi/N;v.append((loc[0]+sc[0]*cos(a)*cos(b),loc[1]+sc[1]*cos(a)*sin(b),loc[2]+sc[2]*sin(a)))
 f=[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)for j in range(M)for i in range(N)]
 ob=mesh(n,v,f,m)
 for face in ob.data.polygons:face.use_smooth=True
 return ob
def chair(x,y,z,angle,m,tall=False):
 before=set(bpy.data.objects)
 coll=box('Chair collision', (0,0,.57),(.76,.76,1.1),m,True);coll['collision_only']=True;coll.hide_render=True;coll.hide_set(True)
 ellipsoid('Sculpted upholstered seat',(0,0,.48),(.42,.39,.12),m)
 # Continuous rounded bucket: side arms rise into the back; Egg variant higher at rear.
 N=36;v=[]
 for j in range(8):
  t=j/7
  for i in range(N+1):
   a=-.32+i/N*(pi+.64);side=max(0,sin(a));height=.25+(.60 if tall else .25)*math.sqrt(side)
   xx=.40*cos(a)*(1+.32*sin(pi*t));yy=.29*sin(a)+.14*t;zz=.49+t*height
   v.append((xx,yy,zz))
 f=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i)for j in range(7)for i in range(N)]
 ob=mesh('Egg lounge shell'if tall else'Bucket chair shell',v,f,m,True);so=ob.modifiers.new('Upholstery thickness','SOLIDIFY');so.thickness=.065;sub=ob.modifiers.new('Soft upholstery','SUBSURF');sub.levels=1;sub.render_levels=1
 for face in ob.data.polygons:face.use_smooth=True
 beam('Swivel stem',(0,0,.08),(0,0,.44),.035,metal)
 for a in [0,pi/2,pi,3*pi/2]:beam('Four star base',(0,0,.10),(.36*cos(a),.36*sin(a),.05),.017,metal)
 for ob in set(bpy.data.objects)-before:
  # Geometry built near origin, so object transform is correct and shared exportable.
  ob.location=(x,y,z);ob.rotation_euler.z=angle
 return
# Magenta high-back seating cluster seen in main atrium photographs.
for x,y,a in [(2,6,.4),(3.6,6.4,-.4),(5.4,6.2,-.8),(7.4,5.8,.5),(8.6,4.3,2.3),(6.6,3.8,2.8),(4.9,4.3,2.8),(2.8,4.0,2.2)]:chair(x,y+1.6,0,a,pink,True)
def table(x,y,z,r=.55):
 coll=beam('Table collision',(x,y,z),(x,y,z+.76),r,white);coll['collision']=True;coll['collision_only']=True;coll.hide_render=True;coll.hide_set(True)
 beam('Round white tabletop',(x,y,z+.72),(x,y,z+.755),r,white);beam('Table pedestal',(x,y,z+.06),(x,y,z+.72),.038,metal);beam('Table base',(x,y,z+.025),(x,y,z+.06),.29,metal)
for x,y in [(11,5),(14,2),(8,9),(-5,4),(-9,4),(16,-3)]:
 table(x,y,0)
 for a in [0,2.1,4.2]:chair(x+.95*cos(a),y+.95*sin(a),0,a-pi/2,blue)
# Pale wood standing collaboration tables along classroom frontage.
for x,y in [(-12,7),(-5,9),(6,10),(13,9.8)]:
 box('Oak collaboration worktop',(x,y,1.05),(2.5,.85,.06),wood,True,.035)
 for dx in [-1.16,1.16]:box('Oak table end panel',(x+dx,y,.52),(.08,.79,1.04),wood,True)
 for dx in [-.8,0,.8]:
  beam('Stool seat',(x+dx,y-.75,.71),(x+dx,y-.75,.76),.22,white);beam('Stool stem',(x+dx,y-.75,.04),(x+dx,y-.75,.72),.025,metal)
# Lime modular seating at eastern end.
for x,y in [(17,3),(17,4),(17,5),(16,5),(15,5)]:
 box('Lime sofa cushion',(x,y,.43),(.97,.93,.24),yellow,True,.10);box('Lime sofa back',(x,y+.38,.77),(.97,.2,.52),yellow,True,.07)
# Limited visible lab write-up desks, repeated family without invented research equipment.
for lev,z in enumerate(FLOORS[1:],2):
 for i in range(3,len(north)-2,4):
  x,y=north[i];y+=1.4
  box(f'L{lev} visible write-up desk',(x,y,z+.76),(1.6,.8,.05),white)
  for dx in [-.7,.7]:box('Desk metal leg',(x+dx,y,z+.38),(.04,.65,.76),metal)
  chair(x,y+.75,z,pi,blue)
 for x,y in [(-13,-3.6),(10,-.8)]:
  table(x,y,z,.58)
  for a in [0,2.1,4.2]:chair(x+.93*cos(a),y+.93*sin(a),z,a-pi/2,pink)
# Gallery closed doors and restrained kitchenette fronts.
C='Doors'
for lev,z in enumerate(FLOORS[1:],2):
 back=offset(south,3.30)
 for i in [3,8,14,21,28,35,42,49]:
  if i>=len(back)-1:continue
  x,y=back[i];d=Vector(back[i+1])-Vector(back[i]);a=math.atan2(d.y,d.x)
  # Door overlaid onto closed partition: no entry into undocumented rooms.
  ob=box(f'L{lev} closed office door {i}',(0,0,1.08),(.93,.065,2.16),wood,True)
  ob.rotation_euler.z=a;ob.location=(x,y,z)
  beam('Door pull',(x+.2,y-.12,z+.87),(x+.2,y-.12,z+1.21),.018,metal)
C='Rooms'
for lev,z in enumerate(FLOORS[1:],2):
 # Lime surfaces at documented end social hubs.
 box(f'L{lev} east lime lobby panel',(18.1,9.6,z+1.6),(.14,2.0,3.2),lime,True)
# L1 closed classroom doors, tall wood leaves & narrow glazed sidelights.
C='Doors'
for i in [6,16,26,35]:
 x,y=offset(north,-5.5)[i];box('Closed classroom oak double door',(x,y-.12,1.20),(1.85,.08,2.40),wood,True)
 for dx in [-.13,.13]:beam('Classroom door pull',(x+dx,y-.20,.90),(x+dx,y-.20,1.35),.02,metal)
C='Architecture'
for x,y in [(-11,9),(-3,10.9),(6,11.8),(14,12.1)]:beam('Round atrium column',(x,y,0),(x,y,4.2),.28,white)['collision']=True
# Exterior context: limited built massing and planting visible through clear glass.
C='Exterior'
for x,y,w,h in [(-35,25,12,16),(5,40,25,18),(40,20,15,22),(35,-30,25,16)]:box('Context building mass',(x,y,h/2),(w,12,h),mat('Context masonry '+str(x),(.35,.32,.28),.9))
for x,y in [(28,-5),(25,-14),(18,-20),(7,-23),(-8,-24),(-27,-2),(-28,12)]:
 beam('Exterior tree trunk',(x,y,0),(x,y,4),.15,wood)
 ellipsoid('Exterior tree canopy',(x,y,4.4),(2.1,2.1,2.6),mat('Tree foliage '+str(x),(.11,.22,.055),.95))
# Lamps and clear lit planes behind the laboratory frontage.
C='Lighting'
for lev,z in enumerate(FLOORS[1:],2):
 for ix in range(0,len(north)-1,5):
  x,y=north[ix];y+=2.8
  box('Visible laboratory linear diffuser',(x,y,z+3.70),(2.8,.11,.035),em)
  bpy.ops.object.light_add(type='AREA',location=(x,y,z+3.63));o=put(bpy.context.object,f'L{lev} laboratory ceiling illumination');o.data.energy=170;o.data.shape='RECTANGLE';o.data.size=3;o.data.size_y=1.8
# Ground-floor terrazzo divisions follow long axis rather than a fake tile texture.
C='Atrium'
for x in range(-15,21,4):
 box('Terrazzo fine division',(x,5,.006),(.008,9,.008),concrete)
