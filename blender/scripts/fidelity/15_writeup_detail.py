exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
def cen(o):return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)if o.type=='MESH'else o.location
# Select only the documented foreground write-up furniture bay on level two.
prefixes=('L2 oak write-up desk','Oak write-up desk end','Task chair','Write-up monitor','Monitor stand')
remove_where(lambda o:o.name.startswith(prefixes) and -16<cen(o).x<-7 and H<cen(o).z<H+2 and 8<cen(o).y<13.7)
C='Furniture';oak=bpy.data.materials['Light rift cut white oak'];teal=bpy.data.materials.get('Write-up turquoise ribbed upholstery')or mat('Write-up turquoise ribbed upholstery',(.005,.24,.31),.56)
# Photo shows a high shared table with continuous oak end panels and sled stools.
x,y,z=-10.5,10.85,H
box('Photographed shared oak high table',(x,y,z+1.045),(2.9,.88,.055),oak,False,.009)
for dx in [-1.41,1.41]:box('Shared oak vertical end panel',(x+dx,y,z+.52),(.065,.85,1.035),oak,False,.004)
box('Shared table inset modesty panel',(x,y+.16,z+.57),(2.77,.035,.78),oak)
box('Shared table brushed cable hatch',(x+.18,y,z+1.075),(.22,.09,.002),metal,False,.007)
for dx in [-.92,0,.92]:
 for side in [-1,1]:
  xx=x+dx;yy=y+side*.74
  # Curved horizontal upholstery ribs; slim chrome sled legs and footrest.
  pts=[];N=10
  for j in range(N):
   t=j/(N-1);zz=z+.74+.41*t;cy=yy+side*(.15+.075*t)
   for k in range(13):
    u=(k/12-.5)*.42;pts.append((xx+u,cy+side*.065*(u/.21)**2,zz))
  faces=[(j*13+k,j*13+k+1,(j+1)*13+k+1,(j+1)*13+k)for j in range(N-1)for k in range(12)]
  ob=mesh('Turquoise stool curved padded back',pts,faces,teal);finish(ob,True);so=ob.modifiers.new('Padded shell','SOLIDIFY');so.thickness=.035
  box('Turquoise stool softly rounded seat',(xx,yy,z+.745),(.43,.40,.075),teal,False,.045)
  for j in range(1,6):
   zz=z+.76+j*.06;cy=yy+side*(.15+.075*(zz-z-.74)/.41)
   curve_tube('Turquoise upholstery restrained horizontal seam',[(xx+u,cy-side*.009+side*.065*(u/.21)**2,zz)for u in [-.2,-.15,-.1,-.05,0,.05,.1,.15,.2]],.0017,teal)
  for s in [-1,1]:curve_tube('High stool chrome sled frame',[(xx+s*.19,yy-side*.13,z+.73),(xx+s*.24,yy-side*.23,z+.025),(xx+s*.24,yy+side*.22,z+.025),(xx+s*.19,yy+side*.15,z+.76)],.009,metal)
  beam('High stool chrome footrest',(xx-.23,yy-side*.21,z+.28),(xx+.23,yy-side*.21,z+.28),.009,metal)
# Ceiling construction: white segmented rafts with dark exposed service voids.
C='Ceiling';service=bpy.data.materials.get('Exposed dark mechanical plenum')or mat('Exposed dark mechanical plenum',(.025,.03,.033),.9)
for ob in bpy.data.objects:
 if ob.name.startswith('Laboratory opaque acoustic closure'):
  ob.data.materials.clear();ob.data.materials.append(service)
 if 'white ceiling raft'in ob.name:
  # Existing 3.85m strips were visually continuous. Narrow to reveal photographed channels.
  center=cen(ob)
  for v in ob.data.vertices:v.co.x=center.x+(v.co.x-center.x)*.87
  ob['reference_refinement']='Ceiling raft channel width from Payette write-up photograph'
line=path_resample(north,27)
for lev,zz in enumerate(FLOORS[1:],2):
 for i in range(1,26,3):
  p=Vector(line[i]);xx=p.x+2.05
  for dy,r in [(2.0,.065),(2.35,.10),(5.0,.07)]:
   beam('Visible exposed service conduit',(xx,p.y+dy,zz+3.60),(xx,p.y+dy+2.5,zz+3.60),r,metal)
  # Panel joints divide each broad cloud, as in the photographed ceiling.
  for dy in [1.6,3.2,4.8,6.4]:
   box('Raft fine panel joint',(p.x,p.y+dy,zz+3.177),(3.3,.004,.002),dark)
# Matte carpet in write-up is a warmer medium gray than the dark social pod carpet.
writecarpet=carpet.copy();writecarpet.name='Write-up warm grey carpet'
for n in writecarpet.node_tree.nodes:
 if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.095,.088,.084,1);n.color_ramp.elements[1].color=(.18,.17,.16,1)
for ob in bpy.data.objects:
 if 'write-up carpet'in ob.name:ob.data.materials.clear();ob.data.materials.append(writecarpet)
def camera(name,loc,target,lens):
 ob=bpy.data.objects[name];ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens
camera('REF04_Writeup',(-14,12.6,H+1.6),(18,9,H+1.6),20)
camera('REF02_Reverse_soffit',(-3.8,-3,2*H+1.6),(15,10,7.5),22)
camera('REF11_End_bridge',(21,1,2*H+1.6),(20,11,2*H+1.6),23)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Write-up reference bay, plenum and camera refinements saved')
