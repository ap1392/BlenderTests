"""Build presentation actors and Sequencer from authoritative Blender manifests."""
import unreal,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
a=json.loads((ROOT/'unreal/source/architecture/manifest.json').read_text())
i=json.loads((ROOT/'unreal/validation/architecture_import.json').read_text())
m=json.loads((ROOT/'unreal/validation/material_build.json').read_text())
c=json.loads((ROOT/'unreal/source/cinematic_camera_manifest.json').read_text())
if not i['complete']or not m['complete']:raise RuntimeError('Import/material build incomplete')
world=unreal.EditorLoadingAndSavingUtils.new_blank_map(False);actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
materials={x['source']:unreal.load_asset(x['asset'])for x in m['materials']}
assets={x['source_batch']:x for x in i['assets']};report={'complete':False,'actors':[],'shots':[]}
mesh_editor=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
warned=set(json.loads((ROOT/'unreal/validation/import_tangent_warnings.json').read_text())['batches'])
normal_rebuild={r['batch'] for r in json.loads((ROOT/'unreal/validation/normal_warning_provenance.json').read_text())['batches']}
def spawn(cls,label,location=(0,0,0),rotation=None):
 actor=actors.spawn_actor_from_class(cls,unreal.Vector(*location),rotation or unreal.Rotator())
 actor.set_actor_location(unreal.Vector(*location),False,True)
 actor.set_actor_rotation(rotation or unreal.Rotator(),True)
 actor.set_actor_scale3d(unreal.Vector(1,1,1))
 actual=actor.get_actor_location()
 if max(abs(x-y)for x,y in zip([actual.x,actual.y,actual.z],location))>.001:raise RuntimeError('Actor placement mismatch: '+label)
 actor.set_actor_label(label);return actor
for b in a['batches']:
 asset=assets[b['asset']];mesh=unreal.load_asset(asset['asset'])
 build=mesh_editor.get_lod_build_settings(mesh,0)
 desired={'use_full_precision_u_vs':True,'use_high_precision_tangent_basis':True,'recompute_normals':b['asset'] in normal_rebuild,'recompute_tangents':True,'remove_degenerates':True}
 if b['asset'] in normal_rebuild:desired['compute_weighted_normals']=True
 if b['asset']in warned:desired['use_mikk_t_space']=False
 changed=False
 for field,value in desired.items():
  if build.get_editor_property(field)!=value:build.set_editor_property(field,value);changed=True
 if changed:mesh_editor.set_lod_build_settings(mesh,0,build)
 slots=list(mesh.static_materials);materials_changed=False
 for idx,slot in enumerate(slots):
  name=str(slot.material_slot_name)
  if name in materials:
   if slot.material_interface!=materials[name]:slot.material_interface=materials[name];materials_changed=True
  else:raise RuntimeError('Unmapped material slot '+name+' on '+b['asset'])
 if materials_changed:mesh.set_editor_property('static_materials',slots)
 unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 actor=spawn(unreal.StaticMeshActor,b['asset']);component=actor.static_mesh_component;component.set_static_mesh(mesh)
 component.set_mobility(unreal.ComponentMobility.STATIC)
 if b['surface_class']=='Glass':component.set_cast_shadow(False)
 actor.set_folder_path('Architecture/L'+str(b['floor'])+'/'+b['system'])
 report['actors'].append({'label':b['asset'],'source_objects':len(b['source_objects']),'normal_rebuild':b['asset'] in normal_rebuild,'render_triangles':mesh.get_num_triangles(0)})
def convert_rotation(e):
 x,y,z=e;cx,sx=math.cos(x),math.sin(x);cy,sy=math.cos(y),math.sin(y);cz,sz=math.cos(z),math.sin(z)
 forward=(-(cz*sy*cx+sz*sx),- (sz*sy*cx-cz*sx),-cy*cx)
 up=(cz*sy*sx-sz*cx,sz*sy*sx+cz*cx,cy*sx)
 return unreal.MathLibrary.make_rot_from_xz(unreal.Vector(forward[0],-forward[1],forward[2]),unreal.Vector(up[0],-up[1],up[2]))

# Initial daylight calibration; visual audit against Cycles remains required.
lighting=json.loads((ROOT/'unreal/source/light_manifest.json').read_text())
for light in lighting['lights']:
 v=light['location_m'];location=(100*v[0],-100*v[1],100*v[2]);rotation=convert_rotation(light['rotation_radians'])
 if light['type']=='SUN':
  actor=spawn(unreal.DirectionalLight,light['name'],location,rotation);component=actor.light_component
  component.set_intensity(10000);component.set_editor_property('atmosphere_sun_light',True)
  component.set_editor_property('light_source_angle',math.degrees(light['angle']))
 elif light['type']=='AREA':
  actor=spawn(unreal.RectLight,light['name'],location,rotation);component=actor.light_component
  component.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);component.set_intensity(light['energy']*20)
  component.set_editor_property('source_width',light['size']*100)
  component.set_editor_property('source_height',(light['size_y']if light['shape']=='RECTANGLE'else light['size'])*100)
  component.set_editor_property('attenuation_radius',4000 if 'Skylight'in light['name']else 650)
 else:continue
 component.set_mobility(unreal.ComponentMobility.MOVABLE);component.set_light_color(unreal.LinearColor(*light['color_linear'],1),False)
 actor.set_folder_path('Lighting/Source Fixtures')
report['lighting']={'source_lights':len(lighting['lights']),'intensity_calibration':'initial; needs rendered review','disk_emitters':'rectangular light approximation; visible fixture geometry preserved'}
spawn(unreal.SkyAtmosphere,'ISEC Sky Atmosphere')
sky=spawn(unreal.SkyLight,'ISEC Daylight Sky');sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
sky.light_component.set_editor_property('real_time_capture',True);sky.light_component.set_intensity(1.7)
pp=spawn(unreal.PostProcessVolume,'ISEC Cinematic Exposure');pp.set_editor_property('unbound',True)
s=pp.settings
for name,value in {'override_auto_exposure_min_brightness':True,'override_auto_exposure_max_brightness':True,'auto_exposure_min_brightness':11.0,'auto_exposure_max_brightness':11.0,'override_auto_exposure_bias':True,'auto_exposure_bias':-2.0,'override_bloom_intensity':True,'bloom_intensity':.1,'override_motion_blur_amount':True,'motion_blur_amount':.2,'override_lumen_reflection_quality':True,'lumen_reflection_quality':2.0,'override_lumen_front_layer_translucency_reflections':True,'lumen_front_layer_translucency_reflections':True,'override_lumen_scene_lighting_quality':True,'lumen_scene_lighting_quality':2.0,'override_lumen_final_gather_quality':True,'lumen_final_gather_quality':2.0}.items():s.set_editor_property(name,value)
pp.settings=s
path='/Game/ISEC/Cinematics/ISEC_72s';tools=unreal.AssetToolsHelpers.get_asset_tools()
seq=unreal.load_asset(path)if unreal.EditorAssetLibrary.does_asset_exist(path)else tools.create_asset('ISEC_72s','/Game/ISEC/Cinematics',unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
for binding in seq.get_bindings():binding.remove()
for track in seq.get_tracks():seq.remove_track(track)
seq.set_display_rate(unreal.FrameRate(24,1));seq.set_tick_resolution_directly(unreal.FrameRate(24000,1));seq.set_playback_start(0);seq.set_playback_end(1728)
cut_track=seq.add_track(unreal.MovieSceneCameraCutTrack)
for shot in c['shots']:
 k=shot['keys'][0];v=k['location_m'];rot=convert_rotation(k['rotation_radians'])
 actor=spawn(unreal.CineCameraActor,shot['name'],(100*v[0],-100*v[1],100*v[2]),rot);actor.set_folder_path('Cinematic Cameras')
 camera=actor.get_cine_camera_component();film=camera.filmback;film.sensor_width=36;film.sensor_height=20.25;camera.filmback=film
 camera.current_focal_length=shot['lens_mm'];camera.current_aperture=8
 focus=camera.focus_settings;focus.focus_method=unreal.CameraFocusMethod.DISABLE;camera.focus_settings=focus
 binding=seq.add_possessable(actor);track=binding.add_track(unreal.MovieScene3DTransformTrack);section=track.add_section()
 first,last=shot['first_frame']-1,shot['last_frame'];section.set_range(first,last);channels=section.get_all_channels()
 for key in shot['keys']:
  p=key['location_m'];r=convert_rotation(key['rotation_radians']);values=[100*p[0],-100*p[1],100*p[2],r.roll,r.pitch,r.yaw,1,1,1]
  for ch,value in zip(channels,values):ch.add_key(unreal.FrameNumber(key['frame']-1),value,interpolation=unreal.MovieSceneKeyInterpolation.LINEAR)
 cut=cut_track.add_section();cut.set_range(first,last);bid=unreal.MovieSceneObjectBindingID();bid.set_editor_property('guid',binding.get_id());cut.set_camera_binding_id(bid)
 report['shots'].append({'name':shot['name'],'start':first,'end_exclusive':last,'lens_mm':shot['lens_mm'],'confidence':shot['confidence']})
if not unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/ISEC/Maps/ISEC_Presentation'):raise RuntimeError('Map save failed')
unreal.EditorAssetLibrary.save_loaded_asset(seq)
report['complete']=True;report['visual_review']='pending';(ROOT/'unreal/validation/scene_build.json').write_text(json.dumps(report,indent=2))
