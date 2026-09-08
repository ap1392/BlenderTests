"""Archive actual source lighting without changing the master."""
import bpy,json
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests');scene=bpy.context.scene
lights=[]
for o in scene.objects:
 if o.type!='LIGHT' or o.hide_render:continue
 d=o.data;r={'name':o.name,'type':d.type,'location_m':list(o.matrix_world.translation),'rotation_radians':list(o.matrix_world.to_euler()),'color_linear':list(d.color),'energy':d.energy}
 for k in ['angle','shape','size','size_y','spread','shadow_soft_size']:
  if hasattr(d,k):r[k]=getattr(d,k)
 lights.append(r)
world=[]
if scene.world and scene.world.use_nodes:
 for n in scene.world.node_tree.nodes:
  r={'type':n.bl_idname,'name':n.name}
  for k in ['sky_type','sun_direction','sun_elevation','sun_rotation','sun_intensity','altitude','air_density','dust_density','ozone_density']:
   if hasattr(n,k):
    v=getattr(n,k);r[k]=list(v)if hasattr(v,'__iter__')and not isinstance(v,str)else v
  r['inputs']={s.name:list(s.default_value)if hasattr(s.default_value,'__iter__')else s.default_value for s in n.inputs if hasattr(s,'default_value')}
  world.append(r)
(ROOT/'unreal/source/light_manifest.json').write_text(json.dumps({'lights':lights,'world_nodes':world,'exposure':scene.view_settings.exposure,'note':'Blender watts are not directly interchangeable with Unreal lux/lumens; positions and orientation are authoritative, intensity needs rendered calibration.'},indent=2,default=list))
print('ISEC_LIGHT_MANIFEST',len(lights),flush=True)
