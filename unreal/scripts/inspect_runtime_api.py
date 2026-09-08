import unreal,json
from pathlib import Path
names=['Material','MaterialEditingLibrary','EditorLoadingAndSavingUtils','EditorActorSubsystem','MovieSceneSequence','MovieSceneSection','MovieSceneScriptingDoubleChannel','MovieSceneObjectBindingID','MoviePipelineOutputSetting','MoviePipelineAntiAliasingSetting','MoviePipelinePIEExecutor','CineCameraComponent','PostProcessSettings','MaterialExpressionNoise','MaterialExpressionThinTranslucentMaterialOutput']
r={}
for n in names:
 c=getattr(unreal,n,None)
 r[n]={'doc':getattr(c,'__doc__',''),'methods':{k:getattr(getattr(c,k),'__doc__','') for k in dir(c)if not k.startswith('_') and k in ['new_blank_map','save_map','create_material_expression','connect_material_expressions','connect_material_property','set_scalar_parameter_value','add_possessable','add_track','make_binding_id','add_key','get_channels','get_all_channels','set_range','set_playback_start','set_playback_end']}}
Path('/Users/aditya2610/Desktop/Projects3/BlenderTests/unreal/validation/runtime_api.json').write_text(json.dumps(r,indent=2))
