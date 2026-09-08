"""First installed-engine check. Imports only the eight validated FBX fixtures.

Run in the full Editor with -ExecutePythonScript=<this file> and -NullRHI.
The commandlet's FBX warning logger attempted to open Slate and crashed.
No finished scene or rendered appearance is claimed by this script.
"""
import unreal,json,traceback,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'unreal/source/smoke'
OUT=ROOT/'unreal/validation';OUT.mkdir(parents=True,exist_ok=True)
report={'engine':unreal.SystemLibrary.get_engine_version(),'status':'running','assets':[]}
commandlet=globals().get('ISEC_COMMANDLET',False)
if not commandlet:unreal.EditorPythonScripting.set_keep_python_script_alive(True)
try:
    manifest=json.loads((FOLDER/'manifest.json').read_text())
    files=json.loads((FOLDER/'file_validation.json').read_text())
    if not files['passed']:raise RuntimeError('Source FBX validation failed')
    assets=unreal.AssetToolsHelpers.get_asset_tools()
    for record in manifest['assets']:
        options=unreal.FbxImportUI()
        options.automated_import_should_detect_type=False
        options.import_as_skeletal=False;options.import_mesh=True
        options.import_materials=False;options.import_textures=False;options.import_animations=False
        options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
        mesh_options=options.static_mesh_import_data
        mesh_options.combine_meshes=False;mesh_options.convert_scene=True
        # These export objects have identity transforms and world-space vertices.
        # Bake the FBX scene's meter-to-centimeter conversion into mesh vertices.
        mesh_options.convert_scene_unit=True;mesh_options.import_uniform_scale=1.0
        mesh_options.transform_vertex_to_absolute=True;mesh_options.bake_pivot_in_vertex=False
        mesh_options.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
        mesh_options.auto_generate_collision=False;mesh_options.build_nanite=False
        task=unreal.AssetImportTask()
        task.filename=str(FOLDER/record['file']);task.destination_path='/Game/ISEC/Validation'
        task.destination_name=record['id'];task.automated=True;task.save=True;task.replace_existing=True
        task.replace_existing_settings=True
        task.options=options;task.factory=unreal.FbxFactory()
        existing_path=task.destination_path+'/'+record['id']
        if unreal.EditorAssetLibrary.does_asset_exist(existing_path):
            existing=unreal.EditorAssetLibrary.load_asset(existing_path)
            stored=existing.get_editor_property('asset_import_data')
            for prop in ['convert_scene','convert_scene_unit','import_uniform_scale','transform_vertex_to_absolute','bake_pivot_in_vertex','normal_import_method','auto_generate_collision','build_nanite']:
                stored.set_editor_property(prop,mesh_options.get_editor_property(prop))
        assets.import_asset_tasks([task])
        objects=[o for o in task.get_objects()if isinstance(o,unreal.StaticMesh)]
        if len(objects)!=1:raise RuntimeError(f'{record["id"]}: expected one StaticMesh, got{len(objects)}')
        mesh=objects[0];box=mesh.get_bounding_box()
        lo=box.min;hi=box.max
        low=[lo.x,lo.y,lo.z];high=[hi.x,hi.y,hi.z]
        entry={'id':record['id'],'asset':mesh.get_path_name(),'bounds_cm':{'min':low,'max':high},
               'extent_cm':[high[j]-low[j]for j in range(3)],
               'material_slots':[str(slot.material_slot_name)for slot in mesh.static_materials]}
        report['assets'].append(entry)
        if record['id']=='SM_CalibrationCube_1m' and any(abs(v-100)>.01 for v in entry['extent_cm']):
            raise RuntimeError('Calibration cube is not100cm on each axis; stopping before further imports')
        (OUT/'smoke_import.json').write_text(json.dumps(report,indent=2))
    cube=next(a for a in report['assets']if a['id']=='SM_CalibrationCube_1m')
    if any(abs(v-100)>.01 for v in cube['extent_cm']):raise RuntimeError('Calibration cube is not100cm on each axis')
    basis={}
    for axis in 'XYZ':
        a=next(x for x in report['assets']if x['id']=='SM_Axis_'+axis)
        b=a['bounds_cm'];distance={'X':2,'Y':3,'Z':4}[axis]
        basis[axis]=[(b['min'][j]+b['max'][j])/(2*distance*100)for j in range(3)]
    report['blender_to_unreal_basis_columns']=basis
    report['status']='imported;100cm cube verified; orientation basis measured'
    report['remaining_checks']=['Compare all bounds using the measured basis','Inspect normals,glass,UVs and two chair instances in a rendered scene','Create CineCamera/Sequencer and write one MRQ frame']
except Exception:
    report['status']='failed';report['error']=traceback.format_exc()
    unreal.log_error(report['error'])
finally:
    (OUT/'smoke_import.json').write_text(json.dumps(report,indent=2))
    # Let Slate tick and expire asynchronous import notifications before teardown.
    # Experiment: immediate quit left text objects alive beyond ICU shutdown.
    exit_after=time.monotonic()+20.0
    def finish_after_notifications(delta):
        if time.monotonic()<exit_after:
            return True
        unreal.log('ISEC_IMPORT_NOTIFICATIONS_DRAINED; requesting normal editor exit')
        unreal.SystemLibrary.quit_editor()
        return False
    if not commandlet:exit_ticker=unreal.register_ticker_callback(finish_after_notifications)
if report['status']=='failed':raise RuntimeError(report['error'])
