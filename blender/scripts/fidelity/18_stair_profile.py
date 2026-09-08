exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Radial stair glass panel','Circular glass clamp','Inset stainless helical handrail','Concealed warm stair stringer light','Stair recessed traction strip','Stair soffit panel joint')))
C='Staircase';ri=1.48;ro=3.0;start=math.radians(-47);traction=bpy.data.materials['Stair charcoal abrasive'];led=bpy.data.materials['Stair warm concealed LED'];led.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=2
for lev in range(1,5):
 a=start;z=FLOORS[lev];az=[(a,z)]
 for g in range(3):
  for j in range(10):a-=math.radians(10.4);z+=H/30;az.append((a,z))
  a-=math.radians(16);az.append((a,z))
 aa=[];raw=[]
 for (a0,z0),(a1,z1)in zip(az,az[1:]):
  for j in range(8):
   t=j/8;aa.append(a0+(a1-a0)*t);raw.append(z0+(z1-z0)*t)
 aa.append(az[-1][0]);raw.append(az[-1][1]);zz=[]
 for i in range(len(raw)):
  r=min(7,i,len(raw)-1-i);weights=[r+1-abs(j)for j in range(-r,r+1)];zz.append(sum(raw[i+j]*w for j,w in zip(range(-r,r+1),weights))/sum(weights))
 # Deterministic common elevation profile for all architectural stair layers.
 ob=bpy.data.objects[f'L{lev+1} continuous stair soffit']
 for i,h in enumerate(zz):
  for j in range(2):ob.data.vertices[i*2+j].co.z=h-.18
 finish(ob,True)
 for r,dr in [(ri,-.065),(ro,.065)]:
  ob=bpy.data.objects[f'L{lev+1} smooth spiral white stringer {r}']
  for i,h in enumerate(zz):
   for j,dz in enumerate([-.25,-.25,.52,.52]):ob.data.vertices[i*4+j].co.z=h+dz
  finish(ob,True);path=[(r*cos(a),r*sin(a))for a in aa]
  for j in range(0,len(aa)-1,8):
   end=min(j+8,len(aa)-1);part=path[j:end+1];ob=ribbon('Radial stair glass panel',part,[h+.53 for h in zz[j:end+1]],.64,.013,glass,False);finish(ob,True)
   a=aa[j];rr=r+(.035 if r==ri else -.035)
   for dz in [.61,.95]:
    p=Vector((rr*cos(a),rr*sin(a),zz[j]+dz));n=Vector((cos(a),sin(a),0));finish(beam('Circular glass clamp',p-n*.017,p+n*.017,.025,metal),True)
  rr=r+(.075 if r==ri else -.075)
  curve_tube('Inset stainless helical handrail',[(rr*cos(a),rr*sin(a),h+1.02)for a,h in zip(aa,zz)],.021,metal)
  curve_tube('Concealed warm stair stringer light',[(rr*cos(a),rr*sin(a),h+.15)for a,h in zip(aa,zz)],.006,led)
 for j,((a0,h0),(a1,h1))in enumerate(zip(az,az[1:])):
  # Three nosing strips also at a landing entrance, not an invented eight-line field.
  for d in [.035,.067,.099]:
   a=a0-d/((ri+ro)/2)
   if a<a1+.01:continue
   pts=[(r*cos(t),r*sin(t))for r,t in [(ri+.09,a),(ro-.09,a),(ro-.09,a-.0045),(ri+.09,a-.0045)]]
   finish(poly('Stair recessed traction strip',pts,h1+.0007,.0007,traction,False))
 for j in [11,22]:
  i=j*8;a=aa[i];h=zz[i];curve_tube('Stair soffit panel joint',[(r*cos(a),r*sin(a),h-.181)for r in [ri+.08,ro-.08]],.0012,traction)
# Small reference-camera scale corrections, while retaining metric stair geometry.
ob=bpy.data.objects['REF05_Lower_stair'];ob.data.lens=37;ob.data.shift_y=-.065
ob=bpy.data.objects['REF06_Upper_reverse'];ob.data.lens=24;ob.rotation_euler=(Vector((1,0,9.2))-ob.location).to_track_quat('-Z','Y').to_euler()
ob=bpy.data.objects['REF08_Stair_overhead'];ob.location=(.75,-.75,24.9);ob.rotation_euler=(Vector((-.8,1.5,10))-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=31
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Common smooth stair profile and three-line nosing detail saved')
