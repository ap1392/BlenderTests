exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Fidelity lower stair tread','Lower stair traction','Lower stair continuous','Lower stair clear glass','Lower stair inset handrail','Lower stair recessed warm')))
C='Staircase';a=math.radians(-47);end=(2.24*cos(a),2.24*sin(a))
# Retain the visible L1 trace. Hidden upper continuation terminates at the shared
# annular start section, not the outer-gallery tongue behind it.
path=P([(875.6,428.5),(870,441),(860,457),(847,472),(835,484)])+[end]
center=path_resample(smooth(path,12),31);left=offset(center,.76);right=offset(center,-.76);heights=[H*i/30 for i in range(31)]
traction=bpy.data.materials['Stair charcoal abrasive'];terrazzo=bpy.data.materials['Wausau E31 light terrazzo']
for j in range(30):
 h=heights[j+1];finish(poly(f'Fidelity lower stair tread {j:02}',[left[j],right[j],right[j+1],left[j+1]],h,H/30+.006,terrazzo))
 for dd in [.07,.14,.21]:
  p=Vector(left[j]).lerp(Vector(left[j+1]),dd);q=Vector(right[j]).lerp(Vector(right[j+1]),dd);curve_tube('Lower stair traction',[(*p,h+.001),(*q,h+.001)],.003,traction)
fine=path_resample(smooth(center,4),181);ll=offset(fine,.78);rr=offset(fine,-.78);hh=[H*i/180 for i in range(181)]
v=[(*p,z-.18)for p,q,z in zip(ll,rr,hh)for p in [p,q]];finish(mesh('Lower stair continuous soffit',v,[(i,i+2,i+3,i+1)for i in range(0,len(v)-2,2)],white),True)
for side in [ll,rr]:
 finish(ribbon('Lower stair continuous sidewall',side,[z-.24 for z in hh],.57,.06,white),True)
 for j in range(0,180,6):
  ob=ribbon('Lower stair clear glass panel',side[j:j+7],[z+.34 for z in hh[j:j+7]],.85,.013,glass,False);finish(ob,True)
  for i,f in enumerate(ob.data.polygons):f.use_smooth=i>=2 and(i-2)%4 in [1,3]
 curve_tube('Lower stair inset handrail',[(*p,z+1.02)for p,z in zip(side,hh)],.021,metal)
 curve_tube('Lower stair recessed warm light',[(*p,z+.13)for p,z in zip(side,hh)],.006,bpy.data.materials['Stair warm concealed LED'])
bpy.context.scene['lower_stair_connection']='Visible L1 trace retained; inferred upper path corrected to upper annulus radial start midpoint(1.528,-1.638,H), removing the former overlapping landing obstruction.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
