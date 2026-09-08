"""ISEC measured-plan reconstruction. Execute in Blender via MCP.
Plan origin (806,480), scale 0.10 m/pixel provisional; see reference notes.
"""
import bpy, math, json, random
from mathutils import Vector
from pathlib import Path
from math import sin,cos,pi
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
DETAIL=globals().get('ISEC_DETAIL',False)
random.seed(26)
# Batch cleanup avoids quadratic per-ID remapping during repeated rebuilds.
bpy.data.batch_remove(list(bpy.data.objects))
bpy.data.batch_remove(list(bpy.data.meshes))
bpy.data.batch_remove(list(bpy.data.materials))
bpy.data.batch_remove([c for c in bpy.data.collections if c.name!='Collection'])
COL={}
for n in ['Architecture','Atrium','Staircase','CurtainWall','Railings','Ceiling','Lighting','Furniture','Exterior','Rooms','Doors','Collision','Cameras','Reference']:
 c=bpy.data.collections.new(n);bpy.context.scene.collection.children.link(c);COL[n]=c
C='Architecture'
def put(o,n,m=None,collision=False):
 o.name=n
 for c in list(o.users_collection):c.objects.unlink(o)
 COL[C].objects.link(o)
 if m:o.data.materials.append(m)
 o['collision']=collision;o['evidence']='PARTIALLY DOCUMENTED';return o
def mat(n,col,rough=.5,metal=0,trans=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Transmission Weight'].default_value=trans;p.inputs['IOR'].default_value=1.46;return m
white=mat('Warm white painted steel and plaster',(.79,.80,.79),.34)
floor=mat('Pale grey terrazzo',(.59,.61,.60),.28)
concrete=mat('Board formed grey concrete',(.39,.41,.39),.82)
metal=mat('Brushed stainless steel',(.43,.47,.49),.23,.8)
dark=mat('Charcoal mullions',(.065,.085,.10),.28,.65)
glass=mat('Clear architectural glazing',(.90,.96,.98),.015,0,.98)
spandrel=mat('Blue grey opaque spandrel',(.10,.19,.23),.24,.3)
wood=mat('Natural oak slats',(.48,.30,.14),.5)
carpet=mat('Charcoal carpet',(.075,.085,.093),.95)
lime=mat('Social hub lime green',(.53,.67,.015),.65)
pink=mat('Magenta upholstery',(.48,.008,.11),.88)
blue=mat('Petrol blue upholstery',(.028,.18,.27),.8)
yellow=mat('Chartreuse upholstery',(.62,.67,.06),.85)
black=mat('Ceiling acoustic backing',(.025,.027,.028),.95)
em=mat('Warm white diffuser',(.9,.93,.88),.4);em.node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(1,.94,.81,1);em.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=3
# Small-scale material surface variation; geometry carries the building identity.
if DETAIL:
 for m,scale,strength in [(concrete,5,.18),(floor,95,.065),(carpet,160,.18),(wood,8,.11)]:
  nt=m.node_tree;p=nt.nodes.get('Principled BSDF');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=.035;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],p.inputs['Normal'])
def mesh(n,v,f,m,coll=False):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);COL[C].objects.link(o);o.data.materials.append(m);o['collision']=coll;return o
def box(n,loc,size,m,coll=False,bevel=0):
 x,y,z=loc;dx,dy,dz=[v/2 for v in size]
 v=[(x+i*dx,y+j*dy,z+k*dz)for k in [-1,1]for j in [-1,1]for i in [-1,1]]
 o=mesh(n,v,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],m,coll)
 if bevel and DETAIL:
  b=o.modifiers.new('Edge finish','BEVEL');b.width=bevel;b.segments=2
 return o
def beam(n,a,b,r,m):
 a,b=Vector(a),Vector(b);d=b-a;d.normalize();u=d.cross(Vector((0,0,1)))
 if u.length<.01:u=d.cross(Vector((0,1,0)))
 u.normalize();w=d.cross(u);N=48 if r>.12 else 12;v=[tuple(p+r*(cos(i*2*pi/N)*u+sin(i*2*pi/N)*w))for p in [a,b]for i in range(N)]
 f=[tuple(range(N-1,-1,-1)),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)]
 return mesh(n,v,f,m)
def poly(n,pts,z,thick,m,coll=True):
 N=len(pts);return mesh(n,[(x,y,z-thick)for x,y in pts]+[(x,y,z)for x,y in pts],[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N)for i in range(N)],m,coll)
def smooth(points,count=8):
 out=[]
 for i in range(len(points)-1):
  p0=Vector(points[max(0,i-1)]);p1=Vector(points[i]);p2=Vector(points[i+1]);p3=Vector(points[min(len(points)-1,i+2)])
  for j in range(count):
   t=j/count;out.append(tuple(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)))
 return out+[points[-1]]
def offset(path,width):
 out=[]
 for i,p in enumerate(path):
  d=Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)]);d.normalize();out.append((p[0]+width*d.y,p[1]-width*d.x))
 return out
def strip(n,path,width,z,thick,m,coll=True):
 return poly(n,path+offset(path,width)[::-1],z,thick,m,coll)
def ribbon(n,path,zs,height,thick,m,coll=True):
 other=offset(path,thick);v=[]
 for p,q,z in zip(path,other,zs):v.extend([(p[0],p[1],z),(q[0],q[1],z),(q[0],q[1],z+height),(p[0],p[1],z+height)])
 f=[(0,3,2,1),(len(v)-4,len(v)-3,len(v)-2,len(v)-1)]
 for i in range(len(path)-1):
  for k in range(4): f.append((i*4+k,i*4+(k+1)%4,(i+1)*4+(k+1)%4,(i+1)*4+k))
 return mesh(n,v,f,m,coll)
def rail(n,path,zs):
 C0=globals()['C'];globals()['C']='Railings'
 ribbon(n+' glass',path,[z+.08 for z in zs],1.03,.016,glass)
 if DETAIL:
  for i in range(0,len(path)-1,2):
   p=path[i];beam(n+' post',(p[0],p[1],zs[i]),(p[0],p[1],zs[i]+1.10),.021,metal)
 for i in range(len(path)-1):beam(n+' cap',(*path[i],zs[i]+1.12),(*path[i+1],zs[i+1]+1.12),.028,metal)
 globals()['C']=C0
# Plan-traced public atrium edges (pixel coordinates transformed to meters).
P=lambda pts:[((x-806)*.10,(480-y)*.10)for x,y in pts]
north=smooth(P([(605,409),(700,382),(800,365),(900,357),(994,357)]),10)
south=smooth(P([(627,487),(663,494),(700,514),(730,547),(740,557),(790,530),(870,485),(945,444),(990,420),(994,398),(994,357)]),6)
west=[north[0],south[0]]
FLOORS=[0,4.2,8.4,12.6,16.8,21.0];ROOF=25.2
C='Atrium'
ground=P([(580,414),(700,382),(800,365),(994,357),(1036,420),(1035,480),(1006,541),(954,588),(881,620),(793,641),(744,623),(750,571),(720,509),(680,465),(608,455)])
# Ground footprint combines the public hall and under-gallery circulation.
poly('L1 atrium terrazzo',ground,0,.28,floor)
strip('L1 public undercroft beneath labs',north,-5.6,0,.28,floor)
C='Architecture'
for k,z in enumerate(FLOORS[1:],2):
 strip(f'L{k} curved office gallery',south,3.4,z,.42,white)
 strip(f'L{k} carpet finish',south,3.35,z+.016,.018,carpet)
 strip(f'L{k} lab frontage floor',north,-6,z,.34,white)
 poly(f'L{k} west bridge',[north[0],south[0],(south[0][0]-3.0,south[0][1]),(north[0][0]-3,north[0][1])],z,.42,white)
 
 rail(f'L{k} office gallery west',[p for p in south if p[0]<(-1.1 if k==2 else 1.35)],[z]*len([p for p in south if p[0]<(-1.1 if k==2 else 1.35)]));rail(f'L{k} office gallery east',[p for p in south if p[0]>3.65],[z]*len([p for p in south if p[0]>3.65]));rail(f'L{k} west bridge',[tuple(Vector(west[0]).lerp(Vector(west[1]),.3)),west[1]],[z]*2)
 # Gallery inner office boundary follows traced edge; closed doors later inset.
 back=offset(south,3.35)
 ribbon(f'L{k} office partition',back,[z]*len(back),3.76,.16,white)
C='CurtainWall'
# Continuous interior curtain wall with transparent vision zones and opaque slab bands.
for k,z in enumerate(FLOORS[1:],2):
 ribbon(f'L{k} glazed lab front',north,[z+.13]*len(north),4.04,.018,glass)
 ribbon(f'L{k} spandrel',north,[z-.65]*len(north),.78,.055,spandrel)
 for h in [.0,.78,3.15,4.15]:ribbon(f'L{k} horizontal glazing transom',north,[z+h]*len(north),.048,.12,dark,False)
 # visible shallow write-up zone, closed against unknown labs
 rear=offset(north,-5.9);ribbon(f'L{k} rear laboratory boundary',rear,[z]*len(rear),4.0,.18,white)
 strip(f'L{k} lab ceiling',north,-5.9,z+3.9,.08,white,False)
 for i,p in enumerate(north):
  beam(f'L{k} vertical mullion {i}',(*p,z),(*p,z+4.2),.031,dark)
# Stair: circle from level 2 upwards, three intermediate flight segments, no central column.
C='Staircase';ri=1.48;ro=3.0;start=math.radians(-47)
for level in range(1,5):
 z0=FLOORS[level];N=30;segments=[];angles=[];heights=[]
 # 3 groups of 10 risers, with enlarged level portions totaling 48 degrees.
 a=start;h=z0
 angles.append(a);heights.append(h)
 for group in range(3):
  for j in range(10):
   a+=math.radians(10.4);h+=4.2/N;angles.append(a);heights.append(h)
  a+=math.radians(16);angles.append(a);heights.append(h)
 for j in range(len(angles)-1):
  a0,a1=angles[j:j+2];z=heights[j+1];pts=[(r*cos(a),r*sin(a))for r,a in [(ri,a0),(ro,a0),(ro,a1),(ri,a1)]];poly(f'L{level+1}-{level+2} tread {j:02}',pts,z,.14,white)
 # Smooth white stringer follows pitch and pauses on landings.
 fine=[];hz=[]
 for j in range(len(angles)-1):
  for s in range(4):
   t=s/4;fine.append(angles[j]*(1-t)+angles[j+1]*t);hz.append(heights[j]*(1-t)+heights[j+1]*t)
 fine.append(angles[-1]);hz.append(heights[-1])
 for r in [ri,ro]:
  path=[(r*cos(a),r*sin(a))for a in fine]
  ribbon(f'L{level+1} spiral white stringer r{r}',path,[z-.26 for z in hz],.68,.06,white)
  ribbon(f'L{level+1} spiral glass r{r}',path,[z+.42 for z in hz],.66,.016,glass)
  for j in range(len(path)-1):beam('Helical stainless handrail',(*path[j],hz[j]+1.08),(*path[j+1],hz[j+1]+1.08),.026,metal)
  if DETAIL:
   for j in range(0,len(path),8):beam('Stair glass fixing',(*path[j],hz[j]+.32),(*path[j],hz[j]+1.06),.016,metal)
 # actual gallery junction as wedge + link from stair to gallery edge
 end=[(ri*cos(start),ri*sin(start)),(ro*cos(start),ro*sin(start)),(3.5,-3.4),(1.7,-4.4)]
 poly(f'L{level+1} stair landing connection',end,z0,.26,white)
poly('L6 stair landing connection',[(ri*cos(start),ri*sin(start)),(ro*cos(start),ro*sin(start)),(3.5,-3.4),(1.7,-4.4)],21,.26,white)
# Lower sculptural stair follows non-circular sweep visible in the L1 plan.
low=smooth([(6.5,4.4),(4,2.7)]+[(1+3.6*cos(t*pi/180),-2+3.6*sin(t*pi/180))for t in range(90,271,15)],4)
lowOuter=offset(low,-1.8)
# Equal distance samples along walking centerline give uniform, navigable risers.
centers=[(Vector(p)+Vector(q))/2 for p,q in zip(low,lowOuter)];cum=[0.0]
for i in range(1,len(centers)):cum.append(cum[-1]+(centers[i]-centers[i-1]).length)
def sample_path(path):
 out=[]
 for j in range(31):
  d=cum[-1]*j/30;i=next((i for i in range(1,len(cum))if cum[i]>=d),len(cum)-1);t=(d-cum[i-1])/max(.00001,cum[i]-cum[i-1]);out.append(tuple(Vector(path[i-1]).lerp(Vector(path[i]),t)))
 return out
low,lowOuter=sample_path(low),sample_path(lowOuter);L=len(low);zs=[4.2*min(i/25,1)for i in range(L)]
for j in range(L-1):poly(f'L1-L2 lower stair tread {j}',[low[j],low[j+1],lowOuter[j+1],lowOuter[j]],zs[j+1],.13,white)
for path in [low,lowOuter]:
 ribbon('Lower stair sculptural stringer',path[:-5],[z-.25 for z in zs[:-5]],.62,.055,white);rail('Lower stair',path[:-5],zs[:-5])
# Concrete oval volume behind lower stair, prominent in photographed atrium.
C='Atrium';core_path=smooth([(1,-3.3),(2.2,-2.8),(2.5,-1.7),(1.8,-.8),(.4,-.6),(-.5,-1.7),(0,-2.9),(1,-3.3)],10)
poly('Board formed concrete stair enclosure',core_path,4.12,4.12,concrete)
# Broad stair from atrium to west bridge.
C='Staircase'
for j in range(28):box(f'West broad stair {j:02}',(-16.8,-.5+j*.275,(j+1)*.15-.075),(3.9,.28,.15),floor,True)
for x in [-18.8,-14.8]:rail('West broad stair',[(x,-.6),(x,7.1)],[0,4.2])
poly('L2 broad stair top landing',[(-23,6.9),(-14.8,6.9),(-14.8,8.7),(-23,8.7)],4.2,.24,white)
# L1 north classrooms: only their documented visible portion, closed boundary at 5.8m depth.
C='Rooms';ribbon('Ground classroom front wall',offset(north,-5.6),[0]*len(north),3.9,.15,white)
for idx in [0,-1]:
 edge=[north[idx],offset(north,-5.6)[idx]];ribbon('Ground undercroft end boundary',edge,[0,0],4.2,.16,white)
# Roof with three curved oculi cut out of actual geometry.
C='Ceiling';roofOutline=north+south[::-1];roof=poly('Atrium roof substrate',roofOutline,ROOF,.35,black,False)
for x,y,rx,ry in [(-12,3,4.1,3.2),(0,2.0,3.9,4.8),(12,8.2,3.0,2.9)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=1,depth=2,location=(x,y,ROOF));cut=bpy.context.object;cut.scale=(rx,ry,1);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);mod=roof.modifiers.new('Documented skylight opening','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=roof;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 path=[(x+rx*cos(t*2*pi/96),y+ry*sin(t*2*pi/96))for t in range(97)];ribbon('Oculus plaster reveal',path,[ROOF-.7]*97,.85,.12,white,False);poly('Skylight glazing',path[:-1],ROOF+.3,.025,glass,False)
# End exterior glazing bounds the hall; modeled context beyond it.
C='Exterior'
westGlass=[(-21,7),(-18,-.7)];eastGlass=[(19,12.1),(23,6),(23,-.5),(20,-6),(15,-10),(7,-14),(-6,-14)]
for path in [westGlass,eastGlass]:
 ribbon('Exterior clear curtain wall',path,[0]*len(path),ROOF,.02,glass)
 for i in range(len(path)-1):
  a,b=Vector(path[i]),Vector(path[i+1]);N=max(1,int((b-a).length/1.5))
  for j in range(N+1):
   p=a.lerp(b,j/N);beam('Exterior mullion',(*p,0),(*p,ROOF),.046,dark)
 for z in FLOORS[1:]:ribbon('Exterior transom',path,[z]*len(path),.075,.14,dark,False)
# Architectural closure along west auditorium edge; no invented auditorium interior.
C='Rooms';aud=smooth([(-21,7),(-21,2.5),(-20,-1),(-14,-1.5),(-9,-2.5),(-6,-5.8),(-5.8,-10),(-6,-14)],10);ribbon('Closed auditorium curved boundary',aud,[0]*len(aud),4.16,.22,white)
C='Exterior';box('Immediate landscape ground',(0,0,-.5),(150,130,.5),mat('Exterior paving',(.31,.33,.31),.9),True)
# Smooth walking collision ramps follow the actual stair walking surface.
C='Collision'
for lev in range(1,5):
 a=start;h=FLOORS[lev];az=[(a,h)]
 for g in range(3):
  for j in range(10):a+=math.radians(10.4);h+=.14;az.append((a,h))
  a+=math.radians(16);az.append((a,h))
 v=[]
 for a,h in az:v.extend([(ri*cos(a),ri*sin(a),h+.015),(ro*cos(a),ro*sin(a),h+.015)])
 ob=mesh(f'Collision upper stair ramp {lev}',v,[(i,i+1,i+3,i+2)for i in range(0,len(v)-2,2)],white,True);ob['collision_only']=True;ob.hide_render=True;ob.hide_set(True)
v=[]
for p,q,h in zip(low,lowOuter,zs):v.extend([(*p,h+.015),(*q,h+.015)])
ob=mesh('Collision lower stair ramp',v,[(i,i+1,i+3,i+2)for i in range(0,len(v)-2,2)],white,True);ob['collision_only']=True;ob.hide_render=True;ob.hide_set(True)
ob=mesh('Collision broad stair ramp',[(-18.7,-.64,0),(-14.9,-.64,0),(-14.9,7.06,4.2),(-18.7,7.06,4.2)],[(0,1,2,3)],white,True);ob['collision_only']=True;ob.hide_render=True;ob.hide_set(True)
# Detailed systems implemented separately below.
if DETAIL:
 exec(compile((ROOT/'blender/scripts/detail_isec.py').read_text(),'detail_isec.py','exec'))
# Embed editable procedural sources and reference metadata in the master.
for source in ['build_isec.py','detail_isec.py','export_web.py']:
 old=bpy.data.texts.get(source)
 if old:bpy.data.texts.remove(old)
 text=bpy.data.texts.new(source);text.write((ROOT/'blender/scripts'/source).read_text())
C='Reference'
for file in ['plan_northeastern_level-1-01-1600x1035.png','plan_northeastern_level-2-01-1600x1035.png','plan_northeastern_level-4-01-1600x1035.png']:
 ob=bpy.data.objects.new('Reference '+file,None);COL[C].objects.link(ob);ob['source']='https://www.payette.com/project/northeasternisec/';ob['file']=str(ROOT/'references/images'/file);ob['scale_status']='Provisional 0.10 m/pixel';ob.hide_render=True;ob.hide_set(True)
(ROOT/'renders/validation/lower_stair_route.json').write_text(json.dumps([[round((p[0]+q[0])/2,5),round(h,5),round(-(p[1]+q[1])/2,5)]for p,q,h in zip(low,lowOuter,zs)]))
# Daylight and neutral architectural lighting.
C='Lighting';world=bpy.context.scene.world or bpy.data.worlds.new('Daylight');bpy.context.scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.72,.82,1,1);world.node_tree.nodes['Background'].inputs[1].default_value=.5
bpy.ops.object.light_add(type='SUN',location=(0,0,30));o=put(bpy.context.object,'Soft daylight');o.rotation_euler=(.25,-.4,-.6);o.data.energy=2.0;o.data.angle=.15
for x,y,energy,size in [(-12,3,2000,7),(0,2,2400,7),(12,8,1600,5)]:
 bpy.ops.object.light_add(type='AREA',location=(x,y,24.9));o=put(bpy.context.object,'Skylight bounce');o.data.energy=energy;o.data.shape='DISK';o.data.size=size
for x in [-14,-4,7,17]:
 bpy.ops.object.light_add(type='AREA',location=(x,4,3.75));o=put(bpy.context.object,'Atrium diffuse fill');o.data.energy=220;o.data.size=5
C='Cameras';cams=[('01_Ground_spiral',(14,8,1.65),(-2,1,7),18),('02_Elevated_atrium',(15,3,5.85),(-6,4,7.4),20),('03_Curtain_wall',(10,0,10.05),(-1,12,12),22),('04_Stair_detail',(6,1,10.05),(0,0,11.5),27),('05_Study_gallery',(-15,-3.5,10.05),(-9,0,10.3),24)]
for name,loc,target,lens in cams:
 bpy.ops.object.camera_add(location=loc);o=put(bpy.context.object,name);o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.clip_end=300
s=bpy.context.scene;s.camera=bpy.data.objects['02_Elevated_atrium'];s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=60;s.view_settings.view_transform='AgX'
# Leave Blender in reference-check camera view.
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='SOLID';a.spaces.active.clip_end=400
s['status']='Plan constrained reconstruction; dimensions provisional';s['floor_heights_m']=FLOORS;s['plan_scale_m_per_pixel']=.10
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/('blender/ISEC_Master.blend' if DETAIL else 'blender/backups/ISEC_01_blockout.blend')))
print('ISEC built',len(s.objects),'objects. Detail:',DETAIL)
