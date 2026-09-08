exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# The corrected plan columns intersected several legacy standing stools. Move
# those complete table/stool groups together, retaining the photographed family.
count=0
for ob in bpy.data.objects:
 if ob.get('ground_furniture_clearance_v53') or not ob.name.startswith(('Ground oak standing worktop','Ground standing table slab end','Tall stool white seat','Tall stool chrome leg')):continue
 p=ob.matrix_world@(sum((Vector(v)for v in ob.bound_box),Vector())/8)
 if p.x>-7:
  ob.location.x+=1.4;ob['ground_furniture_clearance_v53']=True;count+=1
# Replace opaque material behind each narrow door vision strip with a real opening.
C='Rooms';gray=bpy.data.materials['Office charcoal paint']
leaves=[o for o in bpy.data.objects if o.name.startswith('L1 documented classroom closed charcoal door')]
for ob in leaves:
 pts=[ob.matrix_world@v.co for v in ob.data.vertices]
 # The 0.9 m leaf's long horizontal axis follows the frontage tangent.
 center=sum(pts,Vector())/len(pts)
 xy=[Vector((p.x,p.y))for p in pts]
 # Use the published frontage controls for the door tangent.
 controls=P([(650,330),(740,311),(837,297),(928,294),(1016,294)])
 for q,r in zip(controls,controls[1:]):
  if q[0]<=center.x<=r[0]:v=(Vector(r)-Vector(q)).normalized();break
 projections=[p.dot(v)for p in xy];width=max(projections)-min(projections)
 p=Vector((center.x,center.y));left=p-v*width/2;right=p+v*width/2
 vl=p+v*(.20-.065);vr=p+v*(.20+.065)
 for aa,bb,z,h in [(left,right,.01,.84),(left,right,2.27,.39),(left,vl,.85,1.42),(vr,right,.85,1.42)]:
  ribbon('L1 documented classroom charcoal leaf around vision',[tuple(aa),tuple(bb)],[z,z],h,.075,gray)
 bpy.data.objects.remove(ob,do_unlink=True)
bpy.context.scene['ground_clearances_v53']='Legacy standing-table groups shifted 1.4 m along the frontage to clear the newly plan-located columns. Closed classroom door vision panes have real cutouts; room access remains closed.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Cleared standing furniture parts',count,'and opened eight door vision strips')
