"""Validated FBX import in the graphical editor (FBX warnings require Slate)."""
import unreal,json,traceback,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'unreal/source/architecture';OUT=ROOT/'unreal/validation/architecture_import.json'
m=json.loads((SRC/'manifest.json').read_text());check=json.loads((SRC/'file_validation.json').read_text())
if not check['passed']:raise RuntimeError('Export file validation failed')
uv_check=json.loads((SRC/'uv_validation.json').read_text())
if uv_check['collapsed_uv_faces']:raise RuntimeError('Export UV validation failed')
normal_rebuild={r['batch'] for r in json.loads((ROOT/'unreal/validation/normal_warning_provenance.json').read_text())['batches']}
for row in uv_check['results']:
 if row.get('zero_normals') and Path(row['file']).stem not in normal_rebuild:
  raise RuntimeError('Unclassified source normal defect: '+row['file'])
report={'complete':False,'engine':unreal.SystemLibrary.get_engine_version(),'assets':[]}
tools=unreal.AssetToolsHelpers.get_asset_tools()
force_file=ROOT/'unreal/validation/reimport_batches.json'
force=set(json.loads(force_file.read_text()).get('batches',[]))if force_file.exists()else set()
try:
 for a in m['batches']:
  folder='/Game/ISEC/Architecture/L'+str(a['floor'])
  path=folder+'/'+a['asset']
  if unreal.EditorAssetLibrary.does_asset_exist(path)and a['asset']not in force:mesh=unreal.EditorAssetLibrary.load_asset(path)
  else:
   opts=unreal.FbxImportUI();opts.automated_import_should_detect_type=False
   opts.import_as_skeletal=False;opts.import_mesh=True;opts.import_materials=False;opts.import_textures=False;opts.import_animations=False
   opts.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
   d=opts.static_mesh_import_data;d.combine_meshes=False;d.convert_scene=True;d.convert_scene_unit=True;d.import_uniform_scale=1
   d.transform_vertex_to_absolute=True;d.bake_pivot_in_vertex=False;d.auto_generate_collision=False;d.build_nanite=False
   # Blender exports custom normals; let Unreal derive tangents from repaired UVs.
   d.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS if a['asset'] in normal_rebuild else unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
   t=unreal.AssetImportTask();t.filename=str(SRC/a['file']);t.destination_path=folder;t.destination_name=a['asset']
   t.automated=True;t.save=True;t.replace_existing=True;t.replace_existing_settings=True;t.options=opts;t.factory=unreal.FbxFactory()
   tools.import_asset_tasks([t]);objects=[o for o in t.get_objects()if isinstance(o,unreal.StaticMesh)]
   if len(objects)!=1:raise RuntimeError('Expected one mesh for '+a['asset'])
   mesh=objects[0]
   unreal.EditorAssetLibrary.set_metadata_tag(mesh,'ISEC_ImportedSourceSHA256',hashlib.sha256((SRC/a['file']).read_bytes()).hexdigest())
   unreal.EditorAssetLibrary.save_loaded_asset(mesh)
  b=mesh.get_bounding_box();lo=[b.min.x,b.min.y,b.min.z];hi=[b.max.x,b.max.y,b.max.z]
  s=a['bounds_m'];expected_lo=[s['min'][0]*100,-s['max'][1]*100,s['min'][2]*100];expected_hi=[s['max'][0]*100,-s['min'][1]*100,s['max'][2]*100]
  error=max(abs(x-y)for x,y in zip(lo+hi,expected_lo+expected_hi))
  if error>.02:raise RuntimeError(f'{a["asset"]}: bounds error {error} cm')
  slots=[str(x.material_slot_name)for x in mesh.static_materials]
  report['assets'].append({'asset':mesh.get_path_name(),'source_batch':a['asset'],'source_file_current_sha256':hashlib.sha256((SRC/a['file']).read_bytes()).hexdigest(),'imported_source_sha256':unreal.EditorAssetLibrary.get_metadata_tag(mesh,'ISEC_ImportedSourceSHA256') or None,'bounds_max_error_cm':error,'material_slots':slots})
  OUT.write_text(json.dumps(report,indent=2))
 report['complete']=True
except Exception:
 report['error']=traceback.format_exc();raise
finally:OUT.write_text(json.dumps(report,indent=2))
