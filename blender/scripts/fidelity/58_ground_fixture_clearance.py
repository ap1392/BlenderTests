exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Ground undercroft blades are lower than gallery blades: bottom H-.99.
# Housing tops were H-.95, leaving a 40 mm intersection. Lower the complete
# fixture assemblies by 110 mm to achieve the same 70 mm clearance as galleries.
count=0
for ob in bpy.data.objects:
 if ob.name.startswith(('Ground drum luminaire','Ground drum photometric')) and not ob.get('ground_fixture_clearance_v58'):
  ob.location.z-=.11;ob['ground_fixture_clearance_v58']=True;count+=1
C='Lighting'
for ob in list(bpy.data.objects):
 if not ob.name.startswith('Ground drum luminaire housing'):continue
 pts=[ob.matrix_world@v.co for v in ob.data.vertices];top=max(p.z for p in pts);p=sum(pts,Vector())/len(pts)
 for dx in [-.13,.13]:beam('Ground drum fine suspension cable',(p.x+dx,p.y,top),(p.x+dx,p.y,H-.79),.002,metal)
bpy.context.scene['ground_fixture_clearance_v58']='Ground undercroft has a distinct lower ceiling elevation. Complete ground drum assemblies lowered 110 mm, correcting the 40 mm blade overlap and leaving 70 mm physical clearance.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Corrected ground fixture assemblies:',count,'parts')
