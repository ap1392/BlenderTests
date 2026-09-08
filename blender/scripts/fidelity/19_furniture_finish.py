exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
C='Furniture'
# Photo-visible quilted upholstery: shallow padded cells, not a flat cylindrical shell.
original=next(o for o in bpy.data.objects if 'Magenta social bucket shell'in o.name)
old=original.data;N=144;M=64;verts=[]
for j in range(M+1):
 t=j/M
 for i in range(N+1):
  u=i/N;a=-.2+u*(pi+.4);padding=.0035*(sin(pi*((u*9+t*5)%1))**2)*(sin(pi*((u*9-t*5)%1))**2)
  r=.33+.045*t+padding;verts.append((r*cos(a),(.27+.025*t+padding)*sin(a),.46+t*(.22+.16*max(0,sin(a)))))
faces=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i)for j in range(M)for i in range(N)]
ob=mesh('Quilted social chair surface template',verts,faces,pink);finish(ob,True);new=ob.data
for item in bpy.data.objects:
 if item.data==old:item.data=new
bpy.data.objects.remove(ob,do_unlink=True)
# End lounge reference includes taller wing chairs with a separately defined headrest.
# Replace only the overly generic bucket cluster in the documented east glazed lounge.
def cen(o):return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)if o.type=='MESH'else o.location
remove_where(lambda o:o.name.startswith(('Gallery magenta bucket','Gallery circular study table')) and 19<cen(o).x<23.5 and 5<cen(o).y<11)
for lev,z in enumerate(FLOORS[1:],2):
 for y in [6.3,8.0,9.7]:
  x=22.3;before=set(bpy.data.objects)
  # Local chair opens -Y; later rotated toward west, then translated.
  rings=[]
  for j in range(16):
   t=j/15;rings.append([((.36+.055*sin(t*pi))*cos(a),(.27+.04*t)*sin(a),.43+t*(.27+.23*max(0,sin(a))))for a in [-.22+i/48*(pi+.44)for i in range(49)]])
  vv=[v for ring in rings for v in ring];ff=[(j*49+i,j*49+i+1,(j+1)*49+i+1,(j+1)*49+i)for j in range(15)for i in range(48)]
  sh=mesh('East lounge tall wing chair arms',vv,ff,pink);finish(sh,True);so=sh.modifiers.new('Soft upholstered shell','SOLIDIFY');so.thickness=.055
  box('East lounge tall padded back',(0,.32,.91),(.48,.13,.78),pink,False,.095)
  box('East lounge rounded headrest',(0,.33,1.35),(.43,.16,.26),pink,False,.10)
  box('East lounge seat cushion',(0,0,.44),(.58,.49,.12),pink,False,.055)
  beam('East lounge swivel stem',(0,0,.06),(0,0,.4),.022,metal)
  for k in range(4):beam('East lounge polished four star base',(0,0,.06),(.32*cos(k*pi/2+.4),.32*sin(k*pi/2+.4),.03),.013,metal)
  for item in set(bpy.data.objects)-before:item.location=(x,y,z);item.rotation_euler.z=-pi/2
 # Matching two-seat upholstered sofa seen across the foreground of university023.
 x,y=20.3,8.2
 box('East lounge magenta two seat base',(x,y,z+.27),(.79,1.75,.31),pink,False,.06)
 box('East lounge two seat cushion',(x+.02,y,z+.48),(.74,1.64,.13),pink,False,.07)
 box('East lounge sofa padded back',(x-.33,y,z+.73),(.16,1.75,.55),pink,False,.07)
 for yy in [y-.87,y+.87]:box('East lounge sofa gently padded arm',(x,yy,z+.60),(.80,.12,.34),pink,False,.055)
 for xx in [x-.3,x+.3]:
  for yy in [y-.72,y+.72]:beam('East lounge sofa chrome foot',(xx,yy,z+.03),(xx,yy,z+.21),.014,metal)
 finish(beam('East lounge small white table',(21.0,8.1,z+.57),(21.0,8.1,z+.60),.34,white),True);beam('East lounge table pedestal',(21,8.1,z+.04),(21,8.1,z+.57),.022,metal)
# White plaster column feet show a restrained dark base reveal in the reference.
C='Architecture'
for item in list(bpy.data.objects):
 if 'rectangular structural pier'in item.name:
  p=cen(item);bottom=min(v.co.z for v in item.data.vertices);box('Write-up pier dark skirting',(p.x,p.y,bottom+.055),(.557,.657,.11),dark)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Quilted bucket fabric, source-supported east lounge family, column skirting saved')
