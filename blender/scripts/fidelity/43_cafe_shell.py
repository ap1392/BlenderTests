exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Smooth continuous molded seat/back replaces the prototype's four-corner boxed tube.
profile=path_resample(smooth([(-.23,.46),(-.16,.455),(-.03,.45),(.10,.47),(.16,.54),(.20,.68),(.22,.84),(.225,.88)],5),33)
verts=[]
for j,(y,z)in enumerate(profile):
 t=j/(len(profile)-1);width=.235-.018*max(0,(z-.5)/.38)
 for k in range(25):
  u=(k/24-.5)*2;x=width*u;corner=(abs(u)**8)*(.018 if j in [0,32]else 0);yy=y-.028*u*u*max(0,(z-.5)/.38);zz=z+.015*u*u*(1-max(0,(z-.5)/.38))-corner
  verts.append((x,yy,zz))
faces=[(j*25+k,j*25+k+1,(j+1)*25+k+1,(j+1)*25+k)for j in range(32)for k in range(24)]
C='Furniture';ma=bpy.data.materials['Warm white chair shell'];template=mesh('Temporary molded cafe shell master',verts,faces,ma);finish(template,True);data=template.data
for ob in bpy.data.objects:
 if 'Cafe molded white seat back' in ob.name:
  ob.data=data
  for mod in list(ob.modifiers):ob.modifiers.remove(mod)
  mod=ob.modifiers.new('Molded shell thickness','SOLIDIFY');mod.thickness=.012
  mod=ob.modifiers.new('Rounded plastic edge','BEVEL');mod.width=.005;mod.segments=3
bpy.data.objects.remove(template,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
