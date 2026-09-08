"""Evaluated world-space FBX batches with source-object provenance.

Separate floor/system/material classes, small spatial furniture batches, and
individual door parts retain useful presentation hierarchy without15k assets.
Blender geometry and the master file are not modified.
"""
import bpy,json,math,re,hashlib,time,traceback
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
OUT=ROOT/'unreal/source/architecture';OUT.mkdir(parents=True,exist_ok=True)
source=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();H=4.4196
groups={}
for o in source.objects:
    if o.type not in {'MESH','CURVE'}or o.hide_render or o.name.lower().startswith('collision'):continue
    b=[o.matrix_world@Vector(v)for v in o.bound_box]
    center=sum(b,Vector())/8
    floor=max(0,min(6,int(math.floor((center.z+.15)/H))))
    collection=o.users_collection[0].name if o.users_collection else 'Unsorted'
    mats=tuple(slot.material.name if slot.material else 'None'for slot in o.material_slots)
    transparent=any('glass'in m.lower()or'glazing'in m.lower()for m in mats)
    role='Glass'if transparent else'Solid'
    key=(floor,collection,role)
    if collection=='Furniture':key+=(int(center.x//12),int(center.y//12))
    if 'door'in o.name.lower():key+=('Door',o.name)
    groups.setdefault(key,[]).append(o.name)
pending=sorted(groups.items(),key=lambda x:str(x[0]));records=[]
if globals().get('ISEC_UV_REPAIR_ONLY',False):
    audit=json.loads((OUT/'uv_validation.json').read_text())
    bad={r['file'].rsplit('_',2)[-2]for r in audit['results']if r['collapsed_uv_faces']or r.get('zero_normals',0)}
    pending=[(k,n)for k,n in pending if hashlib.sha256(repr(k).encode()).hexdigest()[:10]in bad]
    records=[r for r in json.loads((OUT/'manifest.json').read_text())['batches']if r['file'].rsplit('_',2)[-2]not in bad]
export_failed=False
scratch=bpy.data.scenes.new('ISEC_ARCHITECTURE_EXPORT_TEMP')
scratch.unit_settings.system='METRIC';scratch.unit_settings.scale_length=1
def blank():return {'vertices':[],'faces':[],'uv':[],'normals':[],'smooth':[],'materials':[],'material_index':[],'sources':[]}
def flush(batch,key,part,records=records,scratch=scratch,out=OUT):
    if not batch['vertices']:return
    digest=hashlib.sha256(repr(key).encode()).hexdigest()[:10]
    label='SM_L'+str(key[0]+1)+'_'+re.sub('[^A-Za-z0-9_]','_',key[1])+'_'+key[2]+'_'+digest+'_'+str(part)
    mesh=bpy.data.meshes.new(label);mesh.from_pydata(batch['vertices'],[],batch['faces']);mesh.update()
    for name in batch['materials']:
        material=bpy.data.materials.get(name)
        if material is None:
            material=bpy.data.materials.get('ISEC Export Unassigned') or bpy.data.materials.new('ISEC Export Unassigned')
        mesh.materials.append(material)
    uv=mesh.uv_layers.new(name='UVMap')
    for dst,src in zip(uv.data,batch['uv']):dst.uv=src
    # Explicit corner normals already encode both flat and smooth boundaries.
    # Enable their use on every export face, including very thin flat caps.
    for p,index,smooth in zip(mesh.polygons,batch['material_index'],batch['smooth']):p.material_index=index;p.use_smooth=True
    mesh.normals_split_custom_set(batch['normals'])
    obj=bpy.data.objects.new(label,mesh);scratch.collection.objects.link(obj);scratch.view_layers[0].update()
    try:
        with bpy.context.temp_override(scene=scratch,view_layer=scratch.view_layers[0],
            selected_objects=[obj],selected_editable_objects=[obj],active_object=obj,object=obj):
            obj.select_set(True,view_layer=scratch.view_layers[0]);scratch.view_layers[0].objects.active=obj
            bpy.ops.export_scene.fbx(filepath=str(out/(label+'.fbx')),use_selection=True,object_types={'MESH'},
                global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',
                use_mesh_modifiers=False,use_triangles=True,mesh_smooth_type='FACE',add_leaf_bones=False,bake_anim=False,path_mode='AUTO')
        v=batch['vertices']
        records.append({'asset':label,'file':label+'.fbx','floor':key[0]+1,'system':key[1],'surface_class':key[2],
            'vertices':len(v),'polygons_before_fbx_triangulation':len(batch['faces']),
            'bounds_m':{'min':[min(p[j]for p in v)for j in range(3)],'max':[max(p[j]for p in v)for j in range(3)]},
            'materials':batch['materials'],'source_objects':batch['sources'],'actor_transform':'identity; vertices already in source world space'})
    finally:bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
def next_group(pending=pending,records=records,scratch=scratch,out=OUT,root=ROOT,deps=deps):
    global export_failed
    import bpy,json,time,traceback
    if not pending:
        (out/'manifest.json').write_text(json.dumps({'complete':True,'source_master':'blender/ISEC_Master.blend','revision':'polish67',
            'units':'meters with FBX unit metadata; Unreal scale/basis must follow smoke test',
            'source_object_count':sum(len(r['source_objects'])for r in records),'batches':records},indent=2))
        (out/'progress.json').write_text(json.dumps({'complete':True,'groups_remaining':0,'batches_written':len(records)},indent=2))
        bpy.data.scenes.remove(scratch);print('Architecture FBX export complete:',len(records),'batches');return None
    key,names=pending.pop(0);batch=blank();part=0
    try:
        for name in names:
            o=bpy.data.objects[name]
            mesh=bpy.data.meshes.new_from_object(o.evaluated_get(deps),preserve_all_data_layers=True,depsgraph=deps)
            try:
                if batch['vertices']and len(batch['vertices'])+len(mesh.vertices)>100000:
                    flush(batch,key,part);part+=1;batch=blank()
                mesh.transform(o.matrix_world)
                if o.matrix_world.determinant()<0:mesh.flip_normals()
                mesh.update();offset=len(batch['vertices']);face_start=len(batch['faces'])
                batch['vertices'].extend(tuple(v.co)for v in mesh.vertices)
                material_map={}
                for i,m in enumerate(mesh.materials):
                    matname=m.name if m else 'None'
                    if matname not in batch['materials']:batch['materials'].append(matname)
                    material_map[i]=batch['materials'].index(matname)
                if not material_map:
                    if 'None' not in batch['materials']:batch['materials'].append('None')
                    material_map[0]=batch['materials'].index('None')
                mesh.calc_loop_triangles()
                uv=mesh.uv_layers.active;normals=mesh.corner_normals
                for tri in mesh.loop_triangles:
                    if tri.area<1e-12:continue
                    p=mesh.polygons[tri.polygon_index]
                    batch['faces'].append(tuple(offset+i for i in tri.vertices));batch['smooth'].append(p.use_smooth)
                    batch['material_index'].append(material_map.get(p.material_index,0))
                    n=tri.normal.normalized();ref=Vector((0,0,1))if abs(n.z)<.9 else Vector((1,0,0))
                    tangent=n.cross(ref).normalized();bitangent=n.cross(tangent).normalized()
                    uv_origin=mesh.vertices[tri.vertices[0]].co.copy()
                    face_uv=[tuple(uv.data[loop].uv)for loop in tri.loops]if uv else[]
                    uv_area=abs(sum(face_uv[j][0]*face_uv[(j+1)%len(face_uv)][1]-face_uv[(j+1)%len(face_uv)][0]*face_uv[j][1]for j in range(len(face_uv))))if face_uv else 0
                    for loop in tri.loops:
                        co=mesh.vertices[mesh.loops[loop].vertex_index].co
                        delta=co-uv_origin
                        batch['uv'].append(tuple(uv.data[loop].uv)if uv_area>1e-10 else(delta.dot(tangent),delta.dot(bitangent)))
                        normal=normals[loop].vector
                        batch['normals'].append(tuple(normal if normal.length_squared>1e-12 else tri.normal))
                batch['sources'].append({'name':name,'parent':o.parent.name if o.parent else None,
                    'world_matrix':[list(row)for row in o.matrix_world],'vertex_start':offset,'vertex_count':len(mesh.vertices),
                    'polygon_start':face_start,'polygon_count':len(batch['faces'])-face_start,'original_polygon_count':len(mesh.polygons),'uv_layers':[u.name for u in mesh.uv_layers]})
            finally:bpy.data.meshes.remove(mesh)
        flush(batch,key,part)
        (out/'progress.json').write_text(json.dumps({'complete':False,'groups_remaining':len(pending),'batches_written':len(records)},indent=2))
        return .5
    except Exception:
        export_failed=True
        (out/'error.txt').write_text(traceback.format_exc());bpy.data.scenes.remove(scratch);return None
(OUT/'progress.json').write_text(json.dumps({'complete':False,'groups_remaining':len(pending),'batches_written':0},indent=2))
bpy.app.driver_namespace['isec_architecture_export']=next_group
bpy.app.timers.register(next_group,first_interval=.5)
print('Queued',len(pending),'logical groups for evaluated FBX export')
