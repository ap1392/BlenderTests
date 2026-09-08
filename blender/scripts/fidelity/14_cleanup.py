exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/backups/ISEC_before_slab_unions.blend'),copy=True)
def center(o):return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)if o.type=='MESH'else o.location
# Remove duplicate end guards. The continuous curved office-gallery guard already occupies this edge.
remove_where(lambda o:o.name.startswith('End bridge glass guard'))
# All ground fixtures belong under the laboratory undercroft, not over open atrium.
for o in bpy.data.objects:
 if o.name.startswith(('Ground drum luminaire','Ground drum photometric')):
  p=center(o);near=min(north,key=lambda q:abs(q[0]-p.x));dy=max(0,near[1]+1.1-p.y);o.location.y+=dy
 if 'deep exposed gray ceiling beam'in o.name:o.location.y+=.4
remove_where(lambda o:o.name.startswith(('Lobby drum housing','Lobby drum diffuser','Lobby drum illumination'))and -8<center(o).x<4 and center(o).y<0)
# Coplanar architectural additions are united into continuous public slabs.
for lev,z in enumerate(FLOORS[1:],2):
 main=bpy.data.objects.get(f'L{lev} curved office gallery')
 candidates=[]
 for o in bpy.data.objects:
  if o.type!='MESH'or o==main:continue
  if not (f'L{lev} bounded social alcove floor'in o.name or f'L{lev} corrected end bridge floor'in o.name or o.name==f'L{lev} west bridge' or 'Social pod plan-supported rear public floor'in o.name):continue
  top=max((o.matrix_world@v.co).z for v in o.data.vertices)
  if abs(top-z)<.01:candidates.append(o)
 if not main:continue
 finish(main)
 for o in candidates:
  finish(o);mod=main.modifiers.new('Public slab geometric union','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=o;bpy.context.view_layer.objects.active=main
  try:bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(o,do_unlink=True)
  except Exception as e:main.modifiers.remove(mod);print('Union retained separate for',o.name,str(e))
 main.name=f'L{lev} continuous public gallery slab';finish(main)
# Replace rectangular upholstered seat blocks with rounded cushion surfaces.
C='Furniture'
for o in list(bpy.data.objects):
 if o.type!='MESH'or not any(q in o.name for q in ['Social chair seat','Lounge seat cushion','Tulip seat cushion']):continue
 # Shared instanced data is edited once; all instances inherit the refinement.
 if o.data.get('seat_refined'):continue
 coords=[v.co.copy()for v in o.data.vertices];mins=Vector([min(p[i]for p in coords)for i in range(3)]);maxs=Vector([max(p[i]for p in coords)for i in range(3)]);c=(mins+maxs)/2;r=(maxs-mins)/2
 verts=[];N=40;M=16
 for j in range(M+1):
  a=-pi/2+j*pi/M
  for i in range(N):
   b=i*2*pi/N;verts.append((c.x+r.x*cos(a)*cos(b),c.y+r.y*cos(a)*sin(b),c.z+r.z*sin(a)))
 faces=[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)for j in range(M)for i in range(N)]
 o.data.clear_geometry();o.data.from_pydata(verts,[],faces);o.data.update();o.data['seat_refined']=True;finish(o,True)
 for mod in list(o.modifiers):o.modifiers.remove(mod)
# Downward camera source includes slightly eccentric rings; preserve its landscape aspect.
# Final architecture/view metadata, no browser export in this phase.
bpy.context.scene['fidelity_status']='Active refinement: twelve reference views, architectural corrections and repeated independent critique; not an as-built survey'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Continuous slabs, restrained guard details and furniture cushion cleanup saved')
