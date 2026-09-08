exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Payette L1 plan + built REF02; see atrium/ground_frontage_mapping.md.
remove_where(lambda o:o.name.startswith(('Undercroft round concrete column','Classroom closed pale oak leaf','Classroom full-height glazing','Classroom vertical metal frame','Classroom white header','Classroom rear closure','Observed classroom table','Classroom table frame','Classroom teal chair seat','Classroom chair back','L1 documented classroom')))
oak=bpy.data.materials['Light rift cut white oak'];gray=bpy.data.materials['Office charcoal paint']
C='Architecture'
for x,y in P([(745,334),(837,321),(929,317)]):
 finish(beam('L1 documented classroom round column',(x,y,0),(x,y,H-.12),.375,white),True)
controls=P([(650,330),(740,311),(837,297),(928,294),(1016,294)])
def point(px):
 x=(px-806)*.1
 for a,b in zip(controls,controls[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return Vector((x,a[1]+t*(b[1]-a[1])))
 return Vector(controls[-1])
def segment(lo,hi):
 return [tuple(point(lo))]+[p for p in controls if lo<(p[0]*10+806)<hi]+[tuple(point(hi))]
C='Rooms'
for lo,hi in [(650,656),(732,750),(825,845),(922,938),(1014,1016)]:
 ribbon('L1 documented classroom pale oak partition',segment(lo,hi),[0]*len(segment(lo,hi)),3.08,.16,oak)
ribbon('L1 documented classroom white header',controls,[3.08]*len(controls),H-3.08,.18,white)
rooms=[(656,665,723,732),(750,759,816,825),(845,854,913,922),(938,947,1005,1014)]
for index,(a,b,c,d) in enumerate(rooms,1):
 for lo,hi in [(a,b),(c,d)]:
  pa,pb=point(lo),point(hi);v=(pb-pa).normalized();n=Vector((-v.y,v.x));p=(pa+pb)/2
  ribbon('L1 documented classroom closed charcoal door',[tuple(pa),tuple(pb)],[.01,.01],2.65,.075,gray)
  ribbon('L1 documented classroom oak overdoor',[tuple(pa),tuple(pb)],[2.67,2.67],.41,.14,oak)
  for edge,sign in [(pa,-1),(pb,1)]:
   ribbon('L1 documented classroom narrow oak jamb',[tuple(edge-v*.04),tuple(edge+v*.04)],[0,0],2.67,.14,oak)
  # Narrow light vision strip is photo-supported; exact size is inferred.
  mid=p+v*.20-n*.045
  panel_glass('L1 documented classroom door vision panel',[tuple(mid-v*.065),tuple(mid+v*.065)],.85,2.27)
  handle=p+v*.29-n*.075
  beam('L1 documented classroom steel pull',(*handle,.98),(*handle,1.30),.012,metal)
 # Broad classroom glazing has sparse fine butt joints, unlike the lab curtain wall.
 path=segment(b,c);panel_glass('L1 documented classroom clear glass field',path,.035,3.06)
 for p in path_resample(path,5)[1:-1]:
  beam('L1 documented classroom fine glass joint',(*p,.035),(*p,3.06),.004,dark)
 ribbon('L1 documented classroom glass base channel',path,[.018]*len(path),.024,.035,metal)
 # Bounded room depth is sufficient only for the documented visible table rows.
 pa,pb=point(a),point(d);v=(pb-pa).normalized();n=Vector((-v.y,v.x));origin=(pa+pb)/2
 rear_a=pa+n*5.6;rear_b=pb+n*5.6
 for path in [[tuple(pa),tuple(rear_a)],[tuple(rear_a),tuple(rear_b)],[tuple(pb),tuple(rear_b)]]:
  ribbon('L1 documented classroom bounded opaque return',path,[0,0],H-.1,.14,white)
 def localbox(name,x,y,z,dims,ma):
  ob=box(name,(0,0,0),dims,ma,False,.008);p=origin+v*x+n*y;ob.location=(*p,z);ob.rotation_euler.z=math.atan2(v.y,v.x);return ob
 C='Furniture'
 for y in [1.45,2.90,4.35]:
  for x in [-1.55,1.55]:
   localbox('L1 documented classroom row table',x,y,.74,(2.5,.60,.045),white)
   for dx in [-1.12,1.12]:
    localbox('L1 documented classroom table leg',x+dx,y,.36,(.038,.46,.72),metal)
   for dx in [-.78,0,.78]:
    localbox('L1 documented classroom teal seat',x+dx,y+.59,.46,(.41,.4,.05),blue)
    localbox('L1 documented classroom teal back',x+dx,y+.76,.73,(.41,.04,.44),blue)
 C='Rooms'
bpy.context.scene['ground_frontage_v51']='Four nearly straight classroom glass fields, eight closed charcoal doors, oak surrounds and three white columns located from Payette L1 plan. Heights, narrow vision strips and furnishing rows are photo-informed approximations; hidden interiors remain bounded.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Installed documented four-classroom ground frontage')
