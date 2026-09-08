"""Render a review frame by default; ISEC_RENDER_FULL=1 selects the 72s 4K sequence."""
import unreal,json,os,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
request_path=ROOT/'unreal/validation/render_request.json'
request=json.loads(request_path.read_text()) if request_path.exists() else {}
full=os.environ.get('ISEC_RENDER_FULL')=='1'
OUTPUT=ROOT/'renders/cinematic/unreal'/('frames'if full else'review')
OUTPUT.mkdir(parents=True,exist_ok=True)
report={'complete':False,'full_movie':full,'errors':[],'output_directory':str(OUTPUT)}
REPORT=OUTPUT/'render_status.json'
if not json.loads((ROOT/'unreal/validation/scene_build.json').read_text())['complete']:raise RuntimeError('Scene build incomplete')
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
for command in ['r.Shadow.MaxResolution 512','r.Shadow.MaxCSMResolution 2048']:
 unreal.SystemLibrary.execute_console_command(world,command)
unreal.SystemLibrary.collect_garbage()
unreal.EditorLoadingAndSavingUtils.load_map('/Game/ISEC/Maps/ISEC_Presentation')
sub=unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem);queue=sub.get_queue();queue.delete_all_jobs()
job=queue.allocate_new_job(unreal.MoviePipelineExecutorJob);job.job_name='ISEC 72s 4K'if full else'ISEC Atrium Review'
job.map=unreal.SoftObjectPath('/Game/ISEC/Maps/ISEC_Presentation.ISEC_Presentation');job.sequence=unreal.SoftObjectPath('/Game/ISEC/Cinematics/ISEC_72s.ISEC_72s')
config=job.get_configuration();out=config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
out.output_directory=unreal.DirectoryPath(str(OUTPUT));out.output_resolution=unreal.IntPoint(3840,2160)
out.file_name_format='ISEC_{frame_number}';out.zero_pad_frame_numbers=4;out.auto_version=False;out.override_existing_output=True
out.use_custom_frame_rate=True;out.output_frame_rate=unreal.FrameRate(24,1)
if not full:out.use_custom_playback_range=True;out.custom_start_frame=143;out.custom_end_frame=144
config.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
config.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
aa=config.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
aa.spatial_sample_count=1;aa.temporal_sample_count=8;aa.engine_warm_up_count=8;aa.render_warm_up_count=32 if full else 8;aa.render_warm_up_frames=False
aa.override_anti_aliasing=True;aa.anti_aliasing_method=unreal.AntiAliasingMethod.AAM_TSR
game=config.find_or_add_setting_by_class(unreal.MoviePipelineGameOverrideSetting);game.game_mode_override=unreal.load_class(None,'/Script/MovieRenderPipelineCore.MoviePipelineGameMode');game.cinematic_quality_settings=True
cv=config.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
for name,value in {'r.Lumen.HardwareRayTracing':0.0,'r.ScreenPercentage':100.0,'r.MotionBlurQuality':4.0,'r.Shadow.MaxResolution':1024.0 if full else 512.0,'r.Shadow.MaxCSMResolution':2048.0}.items():cv.add_or_update_console_variable(name,value)
if request.get('prepare_presets'):
 presets=[]
 asset_tools=unreal.AssetToolsHelpers.get_asset_tools()
 for shot in range(6):
  for mode in ['Review','Final']:
   name=f'ISEC_{mode}_{shot+1:02d}';asset_path='/Game/ISEC/Cinematics/'+name
   preset=unreal.load_asset(asset_path) if unreal.EditorAssetLibrary.does_asset_exist(asset_path) else asset_tools.create_asset(name,'/Game/ISEC/Cinematics',unreal.MoviePipelinePrimaryConfig,unreal.MoviePipelinePrimaryConfigFactory())
   preset.copy_from(config)
   setting=preset.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
   start=shot*288 if mode=='Final' else shot*288+143
   end=(shot+1)*288 if mode=='Final' else start+1
   setting.use_custom_playback_range=True;setting.custom_start_frame=start;setting.custom_end_frame=end
   setting.output_directory=unreal.DirectoryPath(str(ROOT/'renders/cinematic/unreal'/('frames' if mode=='Final' else 'review_shots')))
   anti=preset.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
   anti.render_warm_up_count=64 if mode=='Final' else 16
   cvars=preset.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
   cvars.add_or_update_console_variable('r.Shadow.MaxResolution',1024.0 if mode=='Final' else 512.0)
   cvars.add_or_update_console_variable('r.Shadow.MaxCSMResolution',4096.0 if mode=='Final' else 2048.0)
   unreal.EditorAssetLibrary.save_loaded_asset(preset)
   presets.append({'mode':mode,'shot':shot+1,'asset':preset.get_path_name(),'start':start,'end_exclusive':end})
 (ROOT/'unreal/validation/render_presets.json').write_text(json.dumps({'complete':True,'presets':presets},indent=2))
 if request.get('quit_after_prepare'):unreal.SystemLibrary.quit_editor()
else:
 executor=unreal.MoviePipelinePIEExecutor();unreal.isec_render_executor=executor
 started=time.monotonic()
 def save():REPORT.write_text(json.dumps(report,indent=2))
 def error(executor,pipeline,fatal,message):
  report['errors'].append({'fatal':bool(fatal),'message':str(message)});save()
 def finished(executor,success):
  report['complete']=bool(success);report['elapsed_seconds']=time.monotonic()-started
  report['frames_written']=len(list(OUTPUT.glob('ISEC_*.png')));save()
  unreal.log('ISEC_RENDER_FINISHED '+str(report))
  if not os.environ.get('ISEC_EDITOR_SESSION'):unreal.SystemLibrary.quit_editor()
 executor.on_executor_errored_delegate.add_callable_unique(error)
 executor.on_executor_finished_delegate.add_callable_unique(finished)
 save();sub.render_queue_with_executor_instance(executor)
