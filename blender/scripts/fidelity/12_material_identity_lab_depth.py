exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Correct an ambiguous material-prefix lookup: white paint and fixture diffuser are distinct.
for o in bpy.data.objects:
 if o.type not in ['MESH','CURVE']:continue
 for slot in o.material_slots:
  if slot.material==em and not any(s in o.name.lower()for s in ['diffuser','optic']):slot.material=white
bs=white.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.72,.73,.72,1);bs.inputs['Roughness'].default_value=.32
bs=em.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.9,.88,.82,1);bs.inputs['Emission Color'].default_value=(1,.86,.66,1);bs.inputs['Emission Strength'].default_value=5
# Avoid unsupported lamps floating into the open void; lights belong within their ceiling field.
def cen(o):return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)if o.type=='MESH'else o.location
remove_where(lambda o:o.name.startswith(('L2 pendant','L3 pendant','L4 pendant','L5 pendant','L6 pendant','Pendant suspension')))
# Old procedural fixtures only; new verified ceiling groups are retained.
# Reveal the actual green lab backing in front of the opaque rear wall.
for o in bpy.data.objects:
 if 'lime lab accent'in o.name:o.location.y-=.32
# Deeper bench/shelf axis follows the long laboratory islands on the published plans.
remove_where(lambda o:o.name.startswith(('Observed laboratory bench top','Observed double laboratory shelf','Lab shelf upright','Optima bench metal frame')))
C='Furniture';worktop=bpy.data.materials['Warm white laboratory epoxy'];oak=bpy.data.materials['Light rift cut white oak'];line=path_resample(north,27)
for lev,z in enumerate(FLOORS[1:],2):
 for i in range(2,25,2):
  p=Vector(offset(line,-6.7)[i])
  box('Plan-aligned long lab bench',(*p,z+.91),(1.75,5.1,.06),worktop)
  for dx in [-.75,.75]:
   for dy in [-2.35,0,2.35]:box('Long lab bench metal leg',(p.x+dx,p.y+dy,z+.45),(.045,.055,.9),white)
  for h in [1.38,1.83]:box('Lab central spine shelf',(p.x,p.y,z+h),(.50,5.05,.042),white)
  for dy in [-2.2,0,2.2]:box('Lab slim vertical service spine',(p.x,p.y+dy,z+1.42),(.055,.10,1.68),white)
  for dy in [-1.8,1.0]:
   box('Lab visible oak drawer pedestal',(p.x+.38,p.y+dy,z+.40),(.57,.55,.70),oak)
   for h in [.28,.5,.7]:box('Lab drawer restrained reveal',(p.x+.675,p.y+dy,z+h),(.002,.49,.006),dark)
  # Short flexible service loops are directly visible in the university laboratory photos.
  for dy in [-1.6,1.6]:
   points=[(p.x+.06+.10*sin(t*pi),p.y+dy+.07*sin(t*2*pi),z+3.12-.72*sin(t*pi))for t in [j/12 for j in range(13)]]
   curve_tube('Observed ceiling service loop',points,.008,white)
 C='Rooms'
 for i in [5,11,17,23]:
  p=Vector(offset(line,-9.4)[i]);box('Lab photographed green rear field',(*p,z+1.5),(3.1,.035,3.0),lime)
 C='Furniture'
# Frame fixed office door leaves, and enclose behind the social pods to stop sky/horizon leaks.
C='Rooms';gray=bpy.data.materials['Office charcoal paint']
for lev,z in enumerate(FLOORS[1:],2):
 ribbon('Social pod enclosed rear boundary',[(-8,-13.5),(4,-13.5)],[z,z],H-.1,.22,gray)
 ribbon('Social pod enclosed east return',[(4,-13.5),(4,-9.4)],[z,z],H-.1,.20,gray)
# Specific photographic colours, not display-space saturated RGB values.
bs=pink.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.23,.0015,.045,1);pink.diffuse_color=(.23,.0015,.045,1)
bs=carpet.node_tree.nodes.get('Principled BSDF')
for n in carpet.node_tree.nodes:
 if n.type=='VALTORGB':
  n.color_ramp.elements[0].color=(.014,.019,.021,1);n.color_ramp.elements[1].color=(.073,.085,.087,1)
# Camera refinements from independent comparison.
def camera(name,loc,target,lens,shift=0):
 o=bpy.data.objects[name];o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.shift_y=shift
camera('REF03_Social_hub',(-10,-7.5,2*H+1.6),(0,-3,2*H+1.6),25,.02)
camera('REF04_Writeup',(-14,11.1,H+1.6),(18,7.5,H+1.6),20)
camera('REF05_Lower_stair',(8.3,7.1,1.6),(3.5,.5,3.0),27)
camera('REF07_Stair_elevation',(12,4,2*H+1.65),(0,0,2*H+1.8),30)
camera('REF08_Stair_overhead',(.35,-.15,24.9),(-.15,.30,10),28)
o=bpy.data.objects['REF08_Stair_overhead'];o['render_width']=1280;o['render_height']=854
camera('REF09_Ground_wide',(20,12.5,1.3),(-2,4,6.4),17)
# Glass guards: replace segmented metal cap tubes with a single smooth tube per continuous path.
remove_where(lambda o:'office gallery' in o.name and (' post'in o.name or ' cap'in o.name))
C='Railings'
for lev,z in enumerate(FLOORS[1:],2):
 for name,path in [('west',[p for p in south if p[0]<1.35]),('east',[p for p in south if p[0]>3.65])]:
  curve_tube(f'L{lev} gallery smooth stainless handrail {name}',[(*p,z+1.02)for p in path],.022,metal)
  for p in path_resample(path,max(2,int(sum((Vector(b)-Vector(a)).length for a,b in zip(path,path[1:]))/1.3))):
   beam('Gallery discreet glass mount',(*p,z+.02),(*p,z+.14),.018,metal)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Material identity, lab-depth, fixture and camera corrections saved')
