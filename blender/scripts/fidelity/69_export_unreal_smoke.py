"""Small evaluated FBX calibration set. Does not modify the architectural master.

Run after the Cycles queue finishes. Validate these assets in the installed UE
before selecting the final import basis or exporting the complete scene.
"""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
OUT=ROOT/'unreal/source/smoke';OUT.mkdir(parents=True,exist_ok=True)
source_scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
visible=[o for o in source_scene.objects if o.type in {'MESH','CURVE'} and not o.hide_render]
def choose(label,predicate):
    candidates=sorted((o for o in visible if predicate(o)),key=lambda o:o.name)
    if not candidates:raise RuntimeError('No representative source for '+label)
    return candidates[0]
sources=[
    ('StairRibbon',choose('stair ribbon',lambda o:'stringer' in o.name.lower() and 'L3' in o.name)),
    ('CurvedRail',choose('curved rail',lambda o:o.type=='CURVE' and ('handrail' in o.name.lower() or 'guard rail' in o.name.lower()))),
    ('ChairShell',choose('chair shell',lambda o:'tulip' in o.name.lower() and ('shell' in o.name.lower() or 'back' in o.name.lower()))),
    ('Glass',choose('glass',lambda o:'clear vision glass' in o.name.lower())),
]
scratch=bpy.data.scenes.new('ISEC_EXPORT_SMOKE_TEMP')
scratch.unit_settings.system='METRIC';scratch.unit_settings.scale_length=1
records=[]
def bounds(mesh):
    return {'min_m':[min(v.co[j] for v in mesh.vertices)for j in range(3)],
            'max_m':[max(v.co[j] for v in mesh.vertices)for j in range(3)]}
def write_asset(label,mesh,source=None):
    # Procedural Blender parts sometimes have no UVs. Supply non-collapsed
    # face charts on export copies so Unreal can construct valid tangents.
    if not mesh.uv_layers:
        uv=mesh.uv_layers.new(name='ExportFallbackUV')
        for p in mesh.polygons:
            n=p.normal.normalized();ref=Vector((0,0,1))if abs(n.z)<.9 else Vector((1,0,0))
            u=n.cross(ref).normalized();v=n.cross(u).normalized()
            for loop in p.loop_indices:
                co=mesh.vertices[mesh.loops[loop].vertex_index].co
                uv.data[loop].uv=(co.dot(u),co.dot(v))
    obj=bpy.data.objects.new('SM_'+label,mesh);scratch.collection.objects.link(obj)
    try:
        scratch.view_layers[0].update()
        with bpy.context.temp_override(scene=scratch,view_layer=scratch.view_layers[0],
                selected_objects=[obj],selected_editable_objects=[obj],active_object=obj,object=obj):
            for o in scratch.objects:o.select_set(False,view_layer=scratch.view_layers[0])
            obj.select_set(True,view_layer=scratch.view_layers[0]);scratch.view_layers[0].objects.active=obj
            path=OUT/(obj.name+'.fbx')
            bpy.ops.export_scene.fbx(filepath=str(path),use_selection=True,object_types={'MESH'},
                global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',
                axis_forward='-Y',axis_up='Z',use_mesh_modifiers=False,use_triangles=True,
                mesh_smooth_type='FACE',add_leaf_bones=False,bake_anim=False,path_mode='AUTO')
            if b'Vertices'not in path.read_bytes():
                raise RuntimeError('FBX contains no vertex array: '+str(path))
        records.append({'id':obj.name,'file':path.name,'source_object':source.name if source else None,
            'source_world_matrix':[list(row)for row in source.matrix_world]if source else None,
            'geometry_space':'evaluated Blender world coordinates in meters; FBX unit metadata converts once',
            'bounds':bounds(mesh),'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),
            'material_slots':[m.name if m else None for m in mesh.materials],'uv_layers':[u.name for u in mesh.uv_layers]})
    finally:
        bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
def box_mesh(name,lo,hi):
    x,y,z=lo;X,Y,Z=hi
    v=[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
    f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    m=bpy.data.meshes.new(name);m.from_pydata(v,[],f);m.update();return m
try:
    write_asset('CalibrationCube_1m',box_mesh('Cube_1m',(0,0,0),(1,1,1)))
    for axis,lo,hi in [('X',(1.9,-.1,-.1),(2.1,.1,.1)),('Y',(-.1,2.9,-.1),(.1,3.1,.1)),('Z',(-.1,-.1,3.9),(.1,.1,4.1))]:
        write_asset('Axis_'+axis,box_mesh('Axis_'+axis,lo,hi))
    for label,o in sources:
        mesh=bpy.data.meshes.new_from_object(o.evaluated_get(deps),preserve_all_data_layers=True,depsgraph=deps)
        mesh.transform(o.matrix_world)
        if o.matrix_world.determinant()<0:mesh.flip_normals()
        mesh.update();write_asset(label,mesh,o)
    (OUT/'manifest.json').write_text(json.dumps({'status':'exported; Unreal roundtrip NOT yet tested',
        'fbx_axes':{'forward':'-Y','up':'Z'},'source_units':'meters','expected_unreal_cube_side_cm':100,
        'axis_marker_centers_blender_m':{'X':[2,0,0],'Y':[0,3,0],'Z':[0,0,4]},
        'required_checks':['cube side100cm','asymmetric axis centers establish exact basis','all bounds after one unit conversion','curve evaluated to mesh','ribbon normals','glass slot and thickness','chair shell scale and smooth normals'],
        'assets':records},indent=2))
finally:
    bpy.data.scenes.remove(scratch)
print('Exported',len(records),'smoke assets. Unreal import verification pending.')
