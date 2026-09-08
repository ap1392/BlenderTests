exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
random.seed(19)
remove_where(lambda o:COL['Furniture'] in o.users_collection and o.name.startswith(('Round white tabletop','Table pedestal','Table base','Table collision','Oak collaboration worktop','Oak table end panel','Stool seat','Stool stem','Lime sofa')))
C='Furniture';oak=bpy.data.materials['Light rift cut white oak'];grayfabric=bpy.data.materials.get('Pewter lounge upholstery')or mat('Pewter lounge upholstery',(.20,.235,.24),.85);whiteplastic=bpy.data.materials.get('Warm white chair shell')or mat('Warm white chair shell',(.70,.71,.67),.42)
# Every family built at metric furniture scale, then linked instances share geometry.
def instanced_family(builder,name,placements):
 before=set(bpy.data.objects);builder();parts=list(set(bpy.data.objects)-before)
 for index,(x,y,z,angle)in enumerate(placements):
  for part in parts:
   ob=part if index==0 else bpy.data.objects.new(name+' linked',part.data)
   if index:COL[C].objects.link(ob)
   ob.name=name+' '+str(index)+' '+part.name;ob.location=(x,y,z);ob.rotation_euler.z=angle
 return parts

def shell(name,rings,ma,thickness=.045):
 N=len(rings[0]);verts=[p for ring in rings for p in ring];faces=[(j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i)for j in range(len(rings)-1)for i in range(N-1)];ob=mesh(name,verts,faces,ma);finish(ob,True);mod=ob.modifiers.new('Upholstered shell thickness','SOLIDIFY');mod.thickness=thickness;be=ob.modifiers.new('Soft sewn edge','BEVEL');be.width=.015;be.segments=3;return ob

def tall_tulip():
 # Photo-derived enveloping petals, narrow upholstered waist and flared upholstered foot.
 N=64;rings=[]
 for z,rx,ry in [(.035,.37,.30),(.10,.36,.28),(.32,.25,.22),(.49,.24,.24),(.62,.31,.28)]:rings.append([(rx*cos(a*2*pi/N),ry*sin(a*2*pi/N),z)for a in range(N+1)])
 shell('Tulip upholstered pedestal',rings,pink,.025)
 rings=[]
 for j in range(16):
  t=j/15;ring=[]
  for i in range(65):
   a=-.22+i/64*(pi+.44);side=max(0,sin(a));height=.60+1.02*(.70+.30*side);z=.51+(height-.51)*t
   rx=.34+.15*sin(t*pi*.8);ry=.29+.13*t;y=ry*sin(a)+.065*t
   ring.append((rx*cos(a),y,z))
  rings.append(ring)
 shell('Tall tulip enveloping back',rings,pink,.058)
 ob=box('Tulip seat cushion',(0,.035,.47),(.57,.50,.13),pink,False,.13)

def lounge(ma=blue):
 rings=[]
 for j in range(10):
  t=j/9;ring=[]
  for i in range(41):
   a=-.2+i/40*(pi+.4);height=.63+.38*max(0,sin(a));x=(.37+.095*sin(pi*t))*cos(a);y=.29*sin(a)+.1*t;ring.append((x,y,.45+t*(height-.45)))
  rings.append(ring)
 shell('Lounge sculpted wing shell',rings,ma,.055)
 box('Lounge seat cushion',(0,-.025,.43),(.59,.52,.105),ma,False,.11)
 for side in [-1,1]:
  curve_tube('Lounge chrome sled',[(side*.27,-.24,.4),(side*.34,-.36,.05),(side*.34,.31,.05),(side*.24,.20,.4)],.010,metal)

def bucket():
 rings=[]
 for j in range(9):
  t=j/8;ring=[]
  for i in range(45):
   a=-.2+i/44*(pi+.4);ring.append(((.33+.045*t)*cos(a),(.27+.025*t)*sin(a),.46+t*(.22+.16*max(0,sin(a)))))
  rings.append(ring)
 shell('Magenta social bucket shell',rings,pink,.05);box('Social chair seat',(0,-.01,.47),(.50,.43,.09),pink,False,.10)
 beam('Social chair swivel stem',(0,0,.065),(0,0,.43),.021,metal)
 for j in range(4):beam('Social chair cross base',(0,0,.065),(.30*cos(j*pi/2+.4),.30*sin(j*pi/2+.4),.035),.013,metal)

def cafe():
 rings=[]
 for z,w,d,y in [(.43,.22,.21,0),(.49,.24,.22,0),(.64,.23,.05,.17),(.88,.22,.04,.19)]:
  rings.append([(-w,y-d,z),(w,y-d,z),(w,y+d,z),(-w,y+d,z),(-w,y-d,z)])
 shell('Cafe molded white seat back',rings,whiteplastic,.022)
 for dx in [-.18,.18]:
  for dy in [-.16,.16]:beam('Cafe slim tubular leg',(dx,dy,.44),(dx*1.25,dy*1.25,.025),.009,metal)

def table(r=.48):
 finish(beam('Thin white table top',(0,0,.735),(0,0,.760),r,white),True);beam('Table chrome stem',(0,0,.05),(0,0,.735),.021,metal)
 for j in range(4):beam('Table polished cross base',(0,0,.05),(.31*cos(j*pi/2),.31*sin(j*pi/2),.028),.012,metal)
# Ground cluster locations follow the plan circulation and photographed groupings.
tulips=[(5.0,7.2,0,-.8),(6.6,7.1,0,.1),(8.2,7.6,0,.6),(9.3,8.4,0,1.2),(8.8,10.0,0,2.7),(7.0,10.3,0,3.3),(5.3,9.2,0,3.8),(3.8,8.1,0,-.7)]
instanced_family(tall_tulip,'Ground tall magenta tulip',tulips)
bluepos=[];graypos=[];cafepos=[];tables=[]
for x,y in [(13,6),(15,1),(-3,10),(-8,10),(16,9)]:
 tables.append((x,y,0,0))
 for j in range(3):
  a=j*2*pi/3+.2;entry=(x+.86*cos(a),y+.86*sin(a),0,a-pi/2)
  (bluepos if j%2 else graypos).append(entry)
for x,y in [(11,-1),(15,-3),(18,4)]:
 tables.append((x,y,0,0))
 for j in range(4):
  a=j*pi/2;cafepos.append((x+.8*cos(a),y+.8*sin(a),0,a-pi/2))
instanced_family(lambda:lounge(blue),'Petrol lounge',bluepos);instanced_family(lambda:lounge(grayfabric),'Pewter lounge',graypos);instanced_family(cafe,'White cafe chair',cafepos);instanced_family(table,'Ground cafe table',tables)
# Small low round tables between the tulip chairs.
for x,y in [(5.8,8.1),(7.8,8.8),(8.8,7.4)]:
 finish(beam('Tulip small white side table',(x,y,.46),(x,y,.49),.31,white),True);beam('Tulip side table base',(x,y,.02),(x,y,.46),.021,metal)
# Gallery study alcoves and end-lounge conversation clusters.
buckets=[];hubtables=[]
for lev,z in enumerate(FLOORS[1:],2):
 for x,y in [(-5.2,-7.7),(-2.5,-6.6),(21,8),(-21,3)]:
  hubtables.append((x,y,z,0))
  for j in [0,1,2]:
   a=j*2*pi/3;buckets.append((x+.8*cos(a),y+.8*sin(a),z,a-pi/2))
instanced_family(bucket,'Gallery magenta bucket',buckets);instanced_family(table,'Gallery circular study table',hubtables)
# Light oak standing collaboration counters with metal high stools under the classroom edge.
for x,y in [(-12,13.7),(-5,15.5),(3.5,16.8),(12.5,17.4)]:
 box('Ground oak standing worktop',(x,y,1.065),(2.8,.84,.055),oak,False,.018)
 for dx in [-1.32,1.32]:box('Ground standing table slab end',(x+dx,y,.52),(.065,.80,1.04),oak)
 for dx in [-.9,0,.9]:
  beam('Tall stool white seat',(x+dx,y-.72,.745),(x+dx,y-.72,.78),.18,white)
  for sx in [-.13,.13]:
   for sy in [-.13,.13]:beam('Tall stool chrome leg',(x+dx+sx,y-.72+sy,.74),(x+dx+sx*1.25,y-.72+sy*1.25,.025),.011,metal)
# Actual modular lime seating family.
for x,y in [(-13,11),(-12,11),(-11,11),(-10,11),(-10,12),(-10,13)]:
 box('Lime sofa upholstered base',(x,y,.24),(.97,.91,.38),yellow,False,.045);box('Lime sofa seat',(x,y-.07,.45),(.96,.77,.16),yellow,False,.055);box('Lime sofa square back',(x,y+.37,.70),(.97,.17,.62),yellow,False,.045)
# Recessed signage and grouped white spotlights visible in university photos.
C='Lighting';red=bpy.data.materials.get('Exit sign red')or mat('Exit sign red',(.65,.005,.003),.4);bs=red.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(1,.005,.001,1);bs.inputs['Emission Strength'].default_value=1.5
for lev,z in enumerate(FLOORS[1:],2):
 for x,y in [(-21.5,7.13),(21.7,12.24)]:
  box('Exit sign white housing',(x,y,z+2.47),(.35,.055,.19),white)
  cu=bpy.data.curves.new('EXIT lettering','FONT');cu.body='EXIT';cu.align_x='CENTER';cu.size=.115;cu.extrude=.0005;ob=bpy.data.objects.new('Illuminated EXIT lettering',cu);COL[C].objects.link(ob);cu.materials.append(red);ob.location=(x,y-.034,z+2.425);ob.rotation_euler=(pi/2,0,0)
 for x,y in [(-17.6,-.2),(16.8,4.6),(1.2,-3.6)]:
  for j in [-1,0,1]:
   a=Vector((x+j*.18,y,z-.19));b=a+Vector((0,.10,-.15));finish(beam('Triple balcony spotlight housing',a,b,.067,white),True);finish(beam('Balcony spotlight optic',b,b+Vector((0,.005,-.008)),.055,em),True)
# Actual photographic mural has no recovered clean source. Preserve it as an explicitly
# reference-derived visible colour field using the unobstructed upper detail, not people.
C='Rooms';ma=bpy.data.materials.get('Reference-derived kitchenette mural detail')or mat('Reference-derived kitchenette mural detail',(.5,.25,.06),.8)
nt=ma.node_tree;bs=nt.nodes.get('Principled BSDF');im=nt.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(ROOT/'references/images/slide-6-7-1600x900.jpg'),check_existing=True);im.image.pack();nt.links.new(im.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.82
for lev,z in enumerate(FLOORS[1:],2):
 ob=mesh('Kitchenette reference-derived mural',[(.02,-9.27,z+1.14),(3.13,-9.27,z+1.14),(3.13,-9.27,z+2.53),(.02,-9.27,z+2.53)],[(0,1,2,3)],ma)
 uv=ob.data.uv_layers.new(name='Visible unoccluded source crop');coords=[(1085/1600,1-543/900),(1350/1600,1-543/900),(1350/1600,1-440/900),(1085/1600,1-450/900)]
 for i,loop in enumerate(ob.data.loops):uv.data[i].uv=coords[loop.vertex_index]
 ob['evidence']='Reconstruction from unobstructed upper crop of photographed mural; exact original artwork not recovered'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Reference-specific furniture families, fixtures and bounded mural reconstruction saved')
