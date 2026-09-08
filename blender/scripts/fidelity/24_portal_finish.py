exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:'lime portal wall'in o.name or'closed lime portal door'in o.name or o.name.startswith(('Portal narrow vision panel','Portal push bar')))
C='Rooms'
for lev,z in enumerate(FLOORS[1:],2):
 for x,y in [(-22,7.35),(21.4,12.5)]:
  dc=x+.5;left=x-1.8;right=x+1.8;ol=dc-.535;orr=dc+.535
  box('Lime portal left solid jamb',((left+ol)/2,y,z+1.75),(ol-left,.24,3.5),lime)
  box('Lime portal right solid jamb',((orr+right)/2,y,z+1.75),(right-orr,.24,3.5),lime)
  box('Lime portal deep header',(dc,y,z+2.89),(1.07,.24,1.22),lime)
  box('Lime portal recessed closed leaf',(dc,y+.06,z+1.13),(1.01,.06,2.24),lime)
  for dx in [-.515,.515]:box('Lime door frame reveal',(dc+dx,y-.018,z+1.135),(.023,.13,2.27),metal)
  box('Lime door frame head',(dc,y-.018,z+2.27),(1.05,.13,.025),metal)
  # The source's long narrow vision panel lies near the latch side.
  box('Portal narrow dark vision frame',(dc+.30,y+.019,z+1.42),(.115,.018,1.37),dark)
  box('Portal narrow clear vision glass',(dc+.30,y+.007,z+1.42),(.077,.012,1.33),glass)
  beam('Portal stainless push bar',(dc-.39,y-.06,z+.99),(dc+.39,y-.06,z+.99),.018,metal)
  for dx in [-.35,.35]:box('Portal push bar mounting',(dc+dx,y-.01,z+.99),(.045,.10,.055),metal)
  box('Portal door closer',(dc-.26,y-.025,z+2.17),(.22,.045,.045),metal)
  # Room-range labels recovered at the east end, floor digit inferred by repeated numbering.
  if x>0:
   cu=bpy.data.curves.new('East portal room range type','FONT');cu.body=f'{lev}60–{lev}79';cu.align_x='CENTER';cu.size=.14;cu.extrude=.0004;ob=bpy.data.objects.new(f'L{lev} east room range label',cu);COL[C].objects.link(ob);cu.materials.append(dark);ob.location=(x,y-.125,z+2.88);ob.rotation_euler=(pi/2,0,0);ob['evidence']='360–379 visible in university023; other level digits inferred from repeated floor numbering'
  # White vertical return closes the head of the public lounge, rather than a floating panel.
  for xx in [left-.12,right+.12]:box('Portal white exterior reveal',(xx,y+.08,z+1.75),(.18,.65,3.5),white)
C='Lighting'
for lev,z in enumerate(FLOORS[1:],2):
 for j in [-1,0,1]:
  a=Vector((18.85+j*.17,9.1,z-.17));b=a+Vector((.015,-.10,-.17));finish(beam('End lounge triple spotlight housing',a,b,.066,white),True);finish(beam('End lounge triple spotlight optic',b,b+Vector((0,-.005,-.007)),.053,em),True)
# Carpet detail is flecked at centimetre/fibre scale, with restrained tonal variance.
nt=carpet.node_tree
for n in nt.nodes:
 if n.type=='TEX_NOISE'and n.inputs['Scale'].default_value<20:n.inputs['Scale'].default_value=17;n.inputs['Detail'].default_value=3.5
 if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.026,.031,.032,1);n.color_ramp.elements[1].color=(.087,.098,.10,1)
cam=bpy.data.objects['REF07_Stair_elevation'];cam.data.lens=39
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Photographed portal recess, labels, fixtures and carpet scale saved')
