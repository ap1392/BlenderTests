exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
def reset(ma,col,rough,metallic=0):
 nt=ma.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metallic;nt.links.new(bs.outputs['BSDF'],out.inputs['Surface']);ma.diffuse_color=(*col,1);return nt,bs
nt,bs=reset(white,(.72,.73,.72),.32)
nt,bs=reset(concrete,(.27,.28,.27),.80)
tex=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(tex.outputs['Object'],sep.inputs[0]);combine=nt.nodes.new('ShaderNodeCombineXYZ');nt.links.new(sep.outputs['X'],combine.inputs['X']);nt.links.new(sep.outputs['Z'],combine.inputs['Y']);nt.links.new(sep.outputs['Y'],combine.inputs['Z'])
brick=nt.nodes.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=1.65;brick.inputs['Row Height'].default_value=.15;brick.inputs['Mortar Size'].default_value=.002;brick.inputs['Mortar Smooth'].default_value=.003;brick.inputs['Color1'].default_value=(.26,.27,.255,1);brick.inputs['Color2'].default_value=(.40,.41,.39,1);brick.inputs['Mortar'].default_value=(.23,.24,.23,1);nt.links.new(combine.outputs[0],brick.inputs['Vector']);nt.links.new(brick.outputs['Color'],bs.inputs['Base Color'])
noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=110;noise.inputs['Detail'].default_value=2;nt.links.new(tex.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.0017;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
# White terrazzo: millimetric aggregate, restrained polished response.
nt,bs=reset(floor,(.60,.61,.59),.24)
tex=nt.nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=440;tex.inputs['Detail'].default_value=2
ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.28;ramp.color_ramp.elements[0].color=(.42,.43,.41,1);ramp.color_ramp.elements[1].position=.63;ramp.color_ramp.elements[1].color=(.67,.68,.65,1);nt.links.new(tex.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color'])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.07;bump.inputs['Distance'].default_value=.0004;nt.links.new(tex.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
# Mottled commercial carpet, subtle at fibre scale and irregular at tile scale.
nt,bs=reset(carpet,(.07,.077,.078),.95);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.2;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.75;ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.26;ramp.color_ramp.elements[0].color=(.025,.031,.032,1);ramp.color_ramp.elements[1].position=.75;ramp.color_ramp.elements[1].color=(.145,.155,.155,1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);micro=nt.nodes.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=750;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.0007;nt.links.new(micro.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
for ma,lo,hi in [(wood,(.22,.12,.045,1),(.44,.285,.13,1)),(bpy.data.materials['Light rift cut white oak'],(.42,.29,.16,1),(.63,.48,.29,1))]:
 nt,bs=reset(ma,lo[:3],.43);coord=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(55,.8,55);nt.links.new(coord.outputs['Object'],mapping.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2;nt.links.new(mapping.outputs[0],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=lo;ramp.color_ramp.elements[1].color=hi;nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.0007;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
nt,bs=reset(metal,(.55,.57,.58),.26,1)
nt,bs=reset(dark,(.027,.038,.043),.28,.62)
nt,bs=reset(spandrel,(.055,.13,.17),.19,.30)
nt,bs=reset(glass,(.96,.99,1),.018);bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.46
for ma,col in [(pink,(.39,.005,.09)),(blue,(.018,.105,.16)),(yellow,(.52,.60,.045))]:
 nt,bs=reset(ma,col,.85);bs.inputs['Sheen Weight'].default_value=.18;noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=950;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.00035;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
# Ground terrazzo broad sweeping tones, traced from the L1 public-floor band layout.
remove_where(lambda o:o.name.startswith('Curving terrazzo tonal band'))
C='Atrium';bandmat=bpy.data.materials.get('Terrazzo pale gray inlay')or mat('Terrazzo pale gray inlay',(.44,.47,.46),.28)
for idx,width in [(1,1.3),(4,1.1),(7,.85)]:
 path=smooth(P([(612,415+idx*8),(700,390+idx*8),(800,361+idx*8),(920,360+idx*8),(994,373+idx*8)]),10)
 strip('Curving terrazzo tonal band',path,width,.004+idx*.0001,.003,bandmat,False)
# Separate tread terrazzo remains unpatterned light warm white at architectural scale.
# Realistic daylight/fixture hierarchy, no arbitrary ground fill cards.
remove_where(lambda o:o.type=='LIGHT')
C='Lighting';s=bpy.context.scene;world=s.world;world.use_nodes=True;nt=world.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputWorld');bg=nt.nodes.new('ShaderNodeBackground');sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=.58;sky.sun_rotation=2.1;sky.altitude=.05;sky.air_density=1;sky.aerosol_density=1.4;bg.inputs['Strength'].default_value=.16;nt.links.new(sky.outputs[0],bg.inputs[0]);nt.links.new(bg.outputs[0],out.inputs[0])
def area(name,loc,power,size,shape='DISK',color=(1,.91,.79)):
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape=shape;data.size=size;data.color=color;ob=bpy.data.objects.new(name,data);COL[C].objects.link(ob);ob.location=loc;return ob
sun=bpy.data.lights.new('Diffuse afternoon sun','SUN');sun.energy=1.2;sun.angle=.075;ob=bpy.data.objects.new('Diffuse afternoon sun',sun);COL[C].objects.link(ob);ob.rotation_euler=(.35,-.5,2.1)
for x,y,size in [(-12,3.3,5),(0,4,7),(12,8,4.5)]:area('Skylight neutral diffuse contribution',(x,y,ROOF+.9),700,size,color=(.85,.91,1))
# Fixtures have visible housings and diffusers, with measured-scale optical surfaces.
for z,points in [(0,[(x,y,r)for x,y,r in [(-14,11,.6),(-10,12,.45),(-6,13,.8),(-2,14,.6),(3,14,.5),(7,15,.8),(11,15,.65),(16,15,.5),(18,10,.7),(13,10,.55),(8,10,.65),(-1,10,.55)]])]:
 for x,y,r in points:
  h=H-1.12;finish(beam('Ground drum luminaire housing',(x,y,h),(x,y,h+.17),r,white),True);finish(beam('Ground drum luminaire diffuser',(x,y,h-.012),(x,y,h),r*.96,em),True);area('Ground drum photometric proxy',(x,y,h-.025),32,r*1.8)
for lev,z in enumerate(FLOORS[1:],2):
 for x,y,r in [(-21.5,1,.5),(-21,4.5,.72),(21,9,.65),(21,6,.46),(-5,-7.5,.65),(-2,-7.6,.5),(0,-6.9,.74)]:
  h=z+H-.72;finish(beam('Lobby drum housing',(x,y,h),(x,y,h+.17),r,white),True);finish(beam('Lobby drum diffuser',(x,y,h-.015),(x,y,h),r*.96,em),True);area('Lobby drum illumination',(x,y,h-.025),24,r*1.8)
 for i in range(2,len(north)-2,5):
  x,y=north[i];o=area('Write-up indirect pendant light',(x,y+2.0,z+2.96),48,2.7,'RECTANGLE');o.data.size_y=.15;o.rotation_euler.x=pi
 for x,y in [(1,-8.7),(-21,3),(21,7)]:area('Kitchenette and lobby downlight',(x,y,z+2.73),35,1.4)
s.render.engine='CYCLES';s.cycles.max_bounces=10;s.cycles.diffuse_bounces=4;s.cycles.glossy_bounces=4;s.cycles.transmission_bounces=8;s.cycles.transparent_max_bounces=8;s.cycles.use_denoising=True;s.view_settings.view_transform='AgX';s.view_settings.exposure=0;s.view_settings.gamma=1
# Include all reference-reconstruction textures inside master where used.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Architectural material and daylight pass saved')
