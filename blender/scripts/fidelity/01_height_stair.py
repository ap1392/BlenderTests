exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
s=bpy.context.scene
if not s.get('fidelity_height_pass'):
 ratio=H/4.2
 for o in list(s.objects):
  if o.type=='MESH':
   inv=o.matrix_world.inverted();world=o.matrix_world.copy()
   for v in o.data.vertices:
    p=world@v.co;p.z*=ratio;v.co=inv@p
  else:o.location.z*=ratio
 s['fidelity_height_pass']=True;s['floor_heights_m']=FLOORS;s['floor_height_evidence']='BCDC 2013 section,14ft6in; design-stage dimension crosschecked against built proportions'
# Rebuild upper stair shell and tread systems, retaining global placement and floor junctions.
remove_where(lambda o: (o.users_collection and o.users_collection[0].name=='Staircase' and ('spiral' in o.name or 'tread' in o.name and o.name.startswith(('L2-','L3-','L4-','L5-')) or o.name.startswith(('Helical stainless','Stair glass fixing')))))
C='Staircase';ri=1.48;ro=3.;start=math.radians(-47)
traction=bpy.data.materials.get('Stair charcoal abrasive') or mat('Stair charcoal abrasive',(.12,.13,.13),.88)
led=bpy.data.materials.get('Stair warm concealed LED') or mat('Stair warm concealed LED',(.95,.82,.62),.4)
bs=led.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(1,.72,.40,1);bs.inputs['Emission Strength'].default_value=4
for lev in range(1,5):
 a=start;z=FLOORS[lev];az=[(a,z)]
 for g in range(3):
  for j in range(10):a-=math.radians(10.4);z+=H/30;az.append((a,z))
  a-=math.radians(16);az.append((a,z))
 for j,((a0,h0),(a1,h1)) in enumerate(zip(az,az[1:])):
  points=[(r*cos(a),r*sin(a)) for r,a in [(ri+.04,a0),(ro-.04,a0),(ro-.04,a1),(ri+.04,a1)]]
  ob=poly(f'L{lev+1}-{lev+2} terrazzo tread {j:02}',points,h1,.065,floor);finish(ob)
  # Three recessed dark grip lines at each riser; broader landings carry repeated lines.
  for d in ([.035,.067,.099] if h1>h0 else [.05,.10,.15,.20,.25,.30,.35,.40]):
   da=d/((ri+ro)/2);aa=a0-da
   if aa<a1+.01:continue
   pp=[(r*cos(t),r*sin(t))for r,t in [(ri+.09,aa),(ro-.09,aa),(ro-.09,aa-.0045),(ri+.09,aa-.0045)]]
   poly('Stair recessed traction strip',pp,h1+.001,.001,traction,False)
 aa=[];zz=[]
 for (a0,z0),(a1,z1) in zip(az,az[1:]):
  for j in range(8):
   t=j/8;aa.append(a0+(a1-a0)*t);zz.append(z0+(z1-z0)*t)
 aa.append(az[-1][0]);zz.append(az[-1][1])
 # Closed ruled soffit independent from treads, with continuous shading.
 v=[(r*cos(a),r*sin(a),z-.18)for a,z in zip(aa,zz)for r in [ri,ro]]
 ob=mesh(f'L{lev+1} continuous stair soffit',v,[(i,i+2,i+3,i+1)for i in range(0,len(v)-2,2)],white);finish(ob,True)
 for r,dr in [(ri,-.065),(ro,.065)]:
  path=[(r*cos(a),r*sin(a))for a in aa]
  ob=ribbon(f'L{lev+1} smooth spiral white stringer {r}',path,[h-.25 for h in zz],.77,dr,white);finish(ob,True)
  # Real guard has top edge above an inset rail, divided at trapezoidal panels.
  for j in range(0,len(aa)-1,8):
   end=min(j+8,len(aa)-1);part=path[j:end+1]
   ob=ribbon('Radial stair glass panel',part,[h+.53 for h in zz[j:end+1]],.64,.013,glass,False);finish(ob,True)
   a=aa[j];rr=r+(.035 if r==ri else -.035)
   for dz in [.61,.95]:
    p=Vector((rr*cos(a),rr*sin(a),zz[j]+dz));n=Vector((cos(a),sin(a),0));beam('Circular glass clamp',p-n*.017,p+n*.017,.025,metal)
  rr=r+(.075 if r==ri else -.075)
  curve_tube('Inset stainless helical handrail',[(rr*cos(a),rr*sin(a),h+1.02)for a,h in zip(aa,zz)],.021,metal)
  rr=r+(.075 if r==ri else -.075)
  curve_tube('Concealed warm stair stringer light',[(rr*cos(a),rr*sin(a),h+.15)for a,h in zip(aa,zz)],.008,led)
 # Sparse transverse soffit joints at fabrication segments.
 for j in [11,22]:
  a,z=az[j];curve_tube('Stair soffit panel joint',[(r*cos(a),r*sin(a),z-.182)for r in [ri+.08,ro-.08]],.003,traction)
s['fidelity_stair_upper']='Circular topology retained; continuous smooth shell, terrazzo treads,3 grip strips, panelized glass,inset rail and lighting based on Wausau and Payette photos'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Height and upper stair refinement saved',len(s.objects))
