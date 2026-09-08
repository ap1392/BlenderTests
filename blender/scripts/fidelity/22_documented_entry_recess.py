exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('Auditorium board formed concrete east curve','Auditorium high concrete return','Auditorium lower return','Auditorium documented entry')))
C='Atrium';aud=smooth(P([(678,450),(705,453),(730,467),(748,489),(759,518),(762,554),(757,580),(745,604)]),12)
def cut_path(path,ycut):
 for i,(a,b)in enumerate(zip(path,path[1:])):
  if a[1]>=ycut>=b[1]:
   t=(ycut-a[1])/(b[1]-a[1]);p=tuple(Vector(a).lerp(Vector(b),t));return path[:i+1]+[p],[p]+path[i+1:]
 raise RuntimeError('Auditorium cut outside path')
northseg,rest=cut_path(aud,-2);mid,southseg=cut_path(rest,-8.9)
for name,path,base in [('north bearing',northseg,0),('documented entry lintel',mid,2.55),('south bearing',southseg,0)]:
 ob=ribbon('Auditorium board formed concrete east curve '+name,path,[base]*len(path),H+.9-base,.28,concrete);finish(ob,True)
ret=smooth(P([(745,604),(728,618),(707,625)]),10);ob=ribbon('Auditorium lower return',ret,[0]*len(ret),H+.9,.28,concrete);finish(ob,True)
# Closed recessed wall at the documented inner plan line. No unseen room is fabricated.
C='Rooms';back=smooth(P([(711,489),(722,508),(729,522),(736,548),(738,568),(734,590)]),10)
ob=ribbon('Auditorium documented entry warm wood backing',back,[0]*len(back),2.55,.16,wood);finish(ob,True)
outer=[p for p in aud if -8.9<=p[1]<=-2];outline=outer+back[::-1];poly('Auditorium documented entry soffit',outline,2.59,.06,bpy.data.materials['Office charcoal paint'])
# Metal-faced closed service door on the observed recessed line; exact hardware inferred.
x,y=-7.05,-8.9;box('Auditorium documented entry closed service door',(x,y,1.08),(.055,1.1,2.16),bpy.data.materials['Office charcoal paint'])
beam('Auditorium documented entry door pull',(x+.035,y+.37,.87),(x+.035,y+.37,1.14),.012,metal)
C='Lighting'
for x,y in [(-6.5,-3.8),(-5.9,-6.2),(-6.1,-8.2)]:
 finish(beam('Auditorium documented entry ceiling downlight',(x,y,2.51),(x,y,2.53),.055,em),True)
 d=bpy.data.lights.new('Auditorium entry warm downlight','AREA');d.shape='DISK';d.size=.18;d.energy=30;d.color=(1,.75,.46);ob=bpy.data.objects.new('Auditorium entry warm downlight',d);COL[C].objects.link(ob);ob.location=(x,y,2.48)
# Restore metric arclength UVs on rebuilt formwork.
for ob in bpy.data.objects:
 if ob.type!='MESH'or concrete not in list(ob.data.materials)or len(ob.data.vertices)%4:continue
 distances=[0.0]
 for i in range(1,len(ob.data.vertices)//4):distances.append(distances[-1]+(ob.data.vertices[i*4].co-ob.data.vertices[(i-1)*4].co).length)
 uv=ob.data.uv_layers.get('Concrete formwork metric')or ob.data.uv_layers.new(name='Concrete formwork metric')
 for loop in ob.data.loops:uv.data[loop.index].uv=(distances[loop.vertex_index//4],ob.data.vertices[loop.vertex_index].co.z)
 ob.data.uv_layers.active=uv
bpy.context.scene['auditorium_entry_evidence']='Published L1 heavy ground-wall line stops y500..569; Wausau2 verifies elevated concrete over wood recess. Lintel elevation2.55m is inferred.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Plan-supported raised entry segment and bounded recessed wood frontage saved')
