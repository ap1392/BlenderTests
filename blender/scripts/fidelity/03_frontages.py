exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:COL['CurtainWall'] in o.users_collection)
# Remove old write-up furniture, lights and slab undersides inside the former empty strip.
def centroid(o):
 if o.type!='MESH':return o.location
 return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)
remove_where(lambda o:(COL['Furniture'] in o.users_collection and centroid(o).z>H and centroid(o).y>7) or 'laboratory ceiling illumination' in o.name or o.name.startswith('Visible laboratory linear diffuser'))
structure=bpy.data.materials.get('Dark gray laboratory piers') or mat('Dark gray laboratory piers',(.19,.205,.21),.65)
oak=bpy.data.materials.get('Light rift cut white oak') or mat('Light rift cut white oak',(.62,.46,.28),.46)
worktop=bpy.data.materials.get('Warm white laboratory epoxy') or mat('Warm white laboratory epoxy',(.75,.76,.71),.34)
chairmat=bpy.data.materials.get('Graphite task chair') or mat('Graphite task chair',(.08,.095,.10),.8)
# Line positions are arclength spaced, not one mullion per spline sample.
line=path_resample(north,27);backs=offset(line,-9.8)
C='CurtainWall'
for lev,z in enumerate(FLOORS[1:],2):
 finish(ribbon(f'L{lev} corrected blue spandrel',line,[z-1.22]*len(line),1.34,.045,spandrel),True)
 panel_glass(f'L{lev} clear vision glass',line,z+.12,z+H-1.22)
 for h in [.12,H-1.22]:ribbon(f'L{lev} main dark transom',line,[z+h-.025]*len(line),.05,.15,dark,False)
 for i,p in enumerate(line):
  t=Vector(line[min(i+1,26)])-Vector(line[max(0,i-1)]);t.normalize();n=Vector((t.y,-t.x))
  pts=[tuple(Vector(p)+t*.027+n*.07),tuple(Vector(p)-t*.027+n*.07),tuple(Vector(p)-t*.027-n*.07),tuple(Vector(p)+t*.027-n*.07)]
  poly(f'L{lev} rectangular mullion {i}',pts,z+H-1.22,H,dark,False)
 # Fine ceramic frit manifestation zone, sufficiently thin to remain transparent.
 frit=bpy.data.materials.get('Subtle white ceramic frit') or mat('Subtle white ceramic frit',(.65,.70,.72),.55)
 for j in range(29):ribbon('Horizontal ceramic frit line',offset(line,.011),[z+.18+j*.021]*len(line),.0022,.001,frit,False)
 # Actual depth: write-up strip, second glazing, shallow documented lab shell.
 C='Architecture'
 strip(f'L{lev} write-up carpet',line,-3.7,z+.018,.018,carpet)
 strip(f'L{lev} observed lab floor',offset(line,-3.7),-6.1,z,.22,floor)
 C='Rooms';second=offset(line,-3.7)
 panel_glass(f'L{lev} closed lab second glazing',second,z+.04,z+3.18)
 ribbon(f'L{lev} far visible laboratory closure',backs,[z]*len(backs),H-.12,.18,white)
 for i,p in enumerate(second):
  if i%2==0:beam('Lab partition vertical framing',(*p,z),(*p,z+3.18),.019,metal)
 # Clear white rectangular ceiling clouds and deep gray beams, as photographed.
 C='Ceiling'
 for i in range(1,26,3):
  p=Vector(line[i]);q=Vector(offset(line,-8)[i]);mid=(p+q)/2
  box(f'L{lev} white ceiling raft',(mid.x,mid.y,z+3.25),(3.85,7.8,.14),white)
  box(f'L{lev} deep exposed gray ceiling beam',(p.x+.4,p.y+4,z+3.46),(.28,8.5,.48),structure)
 C='Architecture'
 for i in range(3,25,5):
  p=Vector(offset(line,-2.7)[i]);box(f'L{lev} rectangular structural pier',(*p,z+1.67),(.55,.65,3.34),structure)
 C='Furniture'
 # Fixed desks along atrium side with monitors/task chairs rather than lounge seats.
 for i in range(1,25,2):
  p=Vector(offset(line,-1.05)[i]);t=Vector(line[min(i+1,26)])-Vector(line[max(0,i-1)]);t.normalize()
  top=box(f'L{lev} oak write-up desk',(*p,z+.77),(2.5,.86,.065),oak,False,.018)
  for dx in [-1.15,1.15]:box('Oak write-up desk end', (p.x+dx,p.y,z+.38),(.07,.80,.75),oak)
  for dx in [-.62,.62]:
   x=p.x+dx;y=p.y+.9
   box('Task chair upholstered seat',(x,y,z+.46),(.48,.45,.10),chairmat,False,.06)
   box('Task chair mesh back',(x,y+.2,z+.77),(.48,.065,.49),chairmat,False,.055)
   beam('Task chair gas stem',(x,y,z+.12),(x,y,z+.44),.027,metal)
   for a in range(5):beam('Task chair five star base',(x,y,z+.12),(x+.28*cos(a*2*pi/5),y+.28*sin(a*2*pi/5),z+.07),.015,dark)
   box('Write-up monitor',(p.x+dx,p.y-.1,z+1.08),(.49,.035,.30),dark,False,.012)
   beam('Monitor stand',(p.x+dx,p.y-.1,z+.80),(p.x+dx,p.y-.1,z+.94),.02,metal)
 # Only documented shelf and bench structures, no invented scientific equipment.
 for i in range(2,25,3):
  p=Vector(offset(line,-6.2)[i]);box('Observed laboratory bench top',(*p,z+.90),(2.5,2.0,.065),worktop)
  for dx in [-1.14,1.14]:
   for dy in [-.86,.86]:box('Optima bench metal frame',(p.x+dx,p.y+dy,z+.45),(.045,.045,.9),white)
  for h in [1.38,1.84]:box('Observed double laboratory shelf',(p.x,p.y,z+h),(2.5,.40,.045),white)
  for dx in [-1.1,1.1]:box('Lab shelf upright',(p.x+dx,p.y,z+1.38),(.045,.10,1.7),white)
  box('Observed mobile oak casework',(p.x+.4,p.y+.4,z+.4),(.68,.58,.72),oak,False,.015)
 C='Rooms'
 for i in [3,15,24]:
  p=backs[i];box(f'L{lev} lime lab accent',(*p,z+1.55),(2.8,.06,3.1),lime)
 C='Lighting'
 for i in range(1,25,3):
  p=Vector(offset(line,-2.0)[i]);box('Peerless type linear pendant housing',(*p,z+2.85),(3.3,.11,.085),metal)
  box('Linear pendant warm diffuser',(p.x,p.y,z+2.805),(3.2,.085,.012),em)
  for dx in [-1.2,1.2]:beam('Linear pendant suspension',(p.x+dx,p.y,z+2.9),(p.x+dx,p.y,z+3.28),.003,metal)
# Classroom furnishings are shallow visible rows, doors remain closed.
C='Furniture'
for i in range(2,24,3):
 p=Vector(offset(line,-8.7)[i])
 for row in range(3):
  y=p.y+row*1.45;box('Observed classroom table',(p.x,y,.74),(2.4,.60,.04),white)
  for dx in [-1.,1.]:
   beam('Classroom table frame',(p.x+dx,y,.05),(p.x+dx,y,.72),.022,metal)
  for dx in [-.75,0,.75]:
   box('Classroom teal chair seat',(p.x+dx,y+.58,.46),(.41,.40,.05),blue,False,.03)
   box('Classroom chair back',(p.x+dx,y+.75,.73),(.41,.04,.44),blue,False,.035)
# Fix end glazing positions beyond bridge floors, remove tall curtain wall slicing across bridge.
remove_where(lambda o:o.name.startswith(('Exterior clear curtain wall','Exterior mullion','Exterior transom','Context building mass','Exterior tree')))
C='Exterior'
for xx,y0,y1 in [(-23.8,-2,8.5),(23.8,1.5,13.4)]:
 path=[(xx,y0),(xx,y1)];panel_glass('End lobby exterior clear glazing',path,0,ROOF)
 for j in range(int((y1-y0)/1.45)+1):
  y=y0+j*1.45;beam('End facade mullion',(xx,y,0),(xx,y,ROOF),.035,dark)
 for z in FLOORS[1:]:ribbon('End facade transom',path,[z+.05]*2,.065,.12,dark)
C='Architecture'
for lev,z in enumerate(FLOORS[1:],2):
 for path in [[(-20.1,7.1),(-17.9,-.7)],[(18.8,12.3),(19,5.0)]]:
  width= -3.3 if path[0][0]<0 else 4.0
  finish(strip(f'L{lev} restored end bridge floor',path,width,z,.42,white))
  strip(f'L{lev} restored end bridge carpet',path,width,z+.016,.016,carpet)
  # Strong fascia and correct white-framed end-room portal.
  ribbon('End bridge fascia',path,[z-.42]*2,.42,.14,white)
  rail('End bridge glass guard',path,[z,z])
C='Rooms'
for lev,z in enumerate(FLOORS[1:],2):
 for x,y in [(-22,7.35),(21.4,12.5)]:
  box(f'L{lev} lime portal wall',(x,y,z+1.75),(3.6,.24,3.5),lime)
  box(f'L{lev} closed lime portal door',(x+.5,y-.14,z+1.10),(.92,.07,2.2),lime)
  box('Portal narrow vision panel',(x+.56,y-.183,z+1.36),(.12,.013,1.45),glass)
  beam('Portal push bar',(x+.12,y-.21,z+.97),(x+.9,y-.21,z+.97),.018,metal)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Layered frontages and end bridges saved',len(bpy.context.scene.objects))
