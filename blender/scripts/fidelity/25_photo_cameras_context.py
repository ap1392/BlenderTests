exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
def camera(name,loc,target,lens):
 ob=bpy.data.objects[name];ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens
# EXIF focal lengths are actual source metadata; positions remain fitted approximations.
camera('REF05_Lower_stair',(14.5,15.4,1.55),(3.6,.6,2.8),65)
camera('REF07_Stair_elevation',(13.4,14.9,3*H+1.65),(0,0,3*H+.65),58)
camera('REF08_Stair_overhead',(.75,-.75,22.098+1.625),(-.8,1.5,10),18)
camera('REF10_Glass_elevation',(9,-4.76,3*H+1.65),(9,12.3,3*H+1.65),35)
camera('REF11_End_bridge',(14.35,1.04,2*H+1.6),(23.3,8,2*H+2),20)
bpy.data.objects['REF09_Ground_wide'].data.lens=16
for name,lens in [('REF05_Lower_stair',65),('REF06_Upper_reverse',24),('REF07_Stair_elevation',58),('REF08_Stair_overhead',18),('REF09_Ground_wide',16),('REF10_Glass_elevation',35),('REF11_End_bridge',20)]:bpy.data.objects[name]['source_exif_focal_length_mm']=lens
# One evidenced residential frontage across Columbus Avenue, not an invented city.
C='Exterior';brickmat=bpy.data.materials.get('Columbus frontage red brown brick')or mat('Columbus frontage red brown brick',(.19,.075,.045),.87)
nt=brickmat.node_tree;bs=nt.nodes.get('Principled BSDF');co=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');comb=nt.nodes.new('ShaderNodeCombineXYZ');nt.links.new(co.outputs['Object'],sep.inputs[0]);nt.links.new(sep.outputs['Y'],comb.inputs[0]);nt.links.new(sep.outputs['Z'],comb.inputs[1]);brick=nt.nodes.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=.215;brick.inputs['Row Height'].default_value=.073;brick.inputs['Mortar Size'].default_value=.004;brick.inputs['Color1'].default_value=(.18,.065,.035,1);brick.inputs['Color2'].default_value=(.26,.11,.06,1);brick.inputs['Mortar'].default_value=(.22,.21,.18,1);nt.links.new(comb.outputs[0],brick.inputs['Vector']);nt.links.new(brick.outputs['Color'],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.2;bump.inputs['Distance'].default_value=.004;nt.links.new(brick.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
stone=bpy.data.materials.get('Columbus pale stone trim')or mat('Columbus pale stone trim',(.62,.60,.53),.72);frame=bpy.data.materials.get('Columbus warm white window frames')or mat('Columbus warm white window frames',(.72,.74,.70),.35);pane=bpy.data.materials.get('Closed residential window glazing')or mat('Closed residential window glazing',(.085,.12,.13),.16,.35)
before=set(bpy.data.objects);box('Documented Columbus residential frontage mass',(75,41,9.15),(4,25.6,18.3),brickmat)
for level in range(5):
 z=.95+level*3.35
 for bay in range(8):
  y=30.5+bay*3.0;w=1.28 if bay%3 else 1.72
  box('Columbus closed sash window',(72.965,y,z+1.06),(.06,w,1.93),pane)
  for yy in [y-w/2,y+w/2]:box('Columbus white window jamb',(72.915,yy,z+1.06),(.075,.07,2.02),frame)
  for zz in [z+.09,z+1.05,z+2.04]:box('Columbus white sash horizontal rail',(72.911,y,zz),(.077,w,.065),frame)
  if w>1.5:box('Columbus paired window center mullion',(72.91,y,z+1.06),(.078,.07,2.02),frame)
  box('Columbus projecting pale lintel',(72.87,y,z+2.17),(.22,w+.28,.18),stone)
  box('Columbus projecting pale sill',(72.87,y,z-.005),(.23,w+.25,.14),stone)
for z in [3.9,7.25,10.6,13.95,17.9]:box('Columbus restrained stone string course',(72.94,41,z),(.15,25.6,.085),stone)
box('Columbus pale parapet cap',(74.9,41,18.40),(4.3,25.9,.20),stone)
for ob in set(bpy.data.objects)-before:ob['evidence']='Visible Columbus residential frontage; probable780Columbus. Five stories supported by official housing page. Position x73/gap49m, partial8-bayextent/module sizes inferred fromsiteplan andreference023.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Source EXIF camera constraints and bounded documented Columbus facade saved')
