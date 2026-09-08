exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
d=json.loads((ROOT/'references/fidelity/calibration/l2_terrace_union.json').read_text())
def center(o):return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)if o.type=='MESH'else o.location
remove_where(lambda o:o.name=='L2 continuous public gallery slab' or o.name.startswith(('L2 office gallery west glass','L2 gallery smooth stainless handrail west','L2 documented terrace'))or(o.name.startswith('Continuous perimeter white fascia')and abs(center(o).z-(H-.316))<.05))
C='Architecture'
def volume(name,p,top,thick,ma):
 xy=p['vertices'];N=len(xy);vs=[(x,y,top-thick)for x,y in xy]+[(x,y,top)for x,y in xy];fs=[tuple(reversed(f))for f in p['triangles']]+[tuple(i+N for i in f)for f in p['triangles']]
 for ring in p['rings']:
  for a,b in zip(ring,ring[1:]+ring[:1]):fs.append((a,b,b+N,a+N))
 ob=mesh(name,vs,fs,ma);finish(ob);return ob
volume('L2 continuous public gallery slab',d['floor'],H,.42,white)
ma=bpy.data.materials['Write-up warm grey carpet'];volume('L2 documented terrace warm grey floor',d['terrace'],H+.008,.004,ma)
for ring in d['floor']['rings']:
 path=[tuple(d['floor']['vertices'][i])for i in ring];path.append(path[0]);finish(ribbon('L2 documented terrace integrated floor fascia',path,[H-.635]*len(path),.638,.04,white),True)
C='Railings'
for path in d['guards']:
 panel_glass('L2 documented terrace remaining exposed gallery guard',path,H+.016,H+1.11);curve_tube('L2 documented terrace remaining gallery handrail',[(*p,H+1.02)for p in path],.022,metal)
# The L2 plan extends the concrete parapet north-west to the broad-stair arrival.
C='Atrium';path=d['outer'][:3];ob=ribbon('L2 documented terrace north concrete parapet',path,[H]*len(path),.9,.28,concrete);finish(ob,True)
uv=ob.data.uv_layers.new(name='Concrete formwork metric');dist=[0]
for i in range(1,len(path)):dist.append(dist[-1]+(Vector(path[i])-Vector(path[i-1])).length)
for loop in ob.data.loops:uv.data[loop.index].uv=(dist[loop.vertex_index//4],ob.data.vertices[loop.vertex_index].co.z)
# L2 meeting-room frontage follows the actual inner edge, not the repeated L4 offset.
prefixes=('Office glazed public frontage','Closed oak office leaf','Office corrected gray header','Office shallow rear closure','Office shallow interior ceiling','Office silver vertical frame')
remove_where(lambda o:o.name.startswith(prefixes) and H-.05<center(o).z<2*H and center(o).x<-5)
C='Rooms';path=path_resample(smooth(list(reversed(d['inner'])),5),18)
for p,q in zip(path,path[1:]):
 panel_glass('L2 documented terrace closed meeting-room glazing',[p,q],H+.016,H+2.80);beam('L2 documented terrace meeting-room vertical frame',(*p,H),(*p,H+2.82),.02,metal)
ribbon('L2 documented terrace meeting-room opaque head',path,[H+2.8]*len(path),H-2.8,.16,bpy.data.materials['Office charcoal paint'])
back=offset(path,2.0);ribbon('L2 documented terrace bounded meeting-room rear',back,[H]*len(back),H-.15,.15,white)
# Reuse the documented lounge family for the dark chairs visible in university026.
C='Furniture';donor=next(o for o in bpy.data.objects if o.name.startswith('Pewter lounge'))
chairparts=[o for o in bpy.data.objects if o.name.startswith('Pewter lounge')and(o.location-donor.location).length<.01]
tdonor=next(o for o in bpy.data.objects if o.name.startswith('Ground cafe table'))
tableparts=[o for o in bpy.data.objects if o.name.startswith('Ground cafe table')and(o.location-tdonor.location).length<.01]
darkcloth=bpy.data.materials.get('Terrace dark woven lounge cloth')or mat('Terrace dark woven lounge cloth',(.033,.028,.027),.86)
for x,y in [(-15.3,1.2),(-11.5,.5),(-8.3,-1.8),(-6,-5.4)]:
 for j in range(3):
  a=j*2*pi/3+.25
  for part in chairparts:
   ob=part.copy();ob.data=part.data.copy();ob.name='L2 documented terrace dark lounge chair';COL[C].objects.link(ob);ob.location=(x+.85*cos(a),y+.85*sin(a),H);ob.rotation_euler=(0,0,a-pi/2)
   for slot in ob.material_slots:
    if slot.material and 'Pewter'in slot.material.name:slot.material=darkcloth
 for part in tableparts:
  ob=part.copy();ob.data=part.data;ob.name='L2 documented terrace small round white table';COL[C].objects.link(ob);ob.location=(x,y,H);ob.rotation_euler=(0,0,0);ob.scale=(.75,.75,.76)
bpy.context.scene['auditorium_terrace_evidence']='University026 and publishedL2 show occupied warm-grey lounge behind0.9m concrete parapet. L2 floor union and room front corrected; furniture count/placement approximate plan groups. No wall-top roof cap.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
