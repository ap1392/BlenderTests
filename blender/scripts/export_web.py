"""Non-destructive evaluated export: batch by material, preserve editable master.
Collision data uses glTF axes (X,Z,-Y). Run through Blender MCP.
"""
import bpy,json,bmesh,math
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
OUT=ROOT/'web/public/models';OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
# Snapshot saved before optimization; master objects never replaced.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
original=list(s.objects);groups={};cv=[];ct=[];counts={};deps=bpy.context.evaluated_depsgraph_get()
for ob in original:
 if ob.type!='MESH':continue
 ev=ob.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();wv=[ob.matrix_world@v.co for v in me.vertices]
 # Normalize normals from geometry after joining; master remains editable.
 for tri in ([] if ob.get('collision_only',False) else me.loop_triangles):
  ma=ob.data.materials[tri.material_index] if len(ob.data.materials)>tri.material_index else None
  if not ma:continue
  # identical concrete joints share one export material
  key='Concrete joint 1' if ma.name.startswith('Concrete joint ')else ma.name
  g=groups.setdefault(key,{'m':ma,'v':[],'f':[]});base=len(g['v']);g['v'].extend([tuple(wv[i])for i in tri.vertices]);g['f'].append((base,base+1,base+2))
 if ob.get('collision',False) and 'tread' not in ob.name and not ob.name.startswith('West broad stair'):
  # exclude tiny tessellated upholstery: coarse furniture solids below instead
  if 'shell' not in ob.name.lower():
   base=len(cv)//3
   for v in wv:cv.extend((round(v.x,5),round(v.z,5),round(-v.y,5)))
   for tri in me.loop_triangles:ct.extend(base+i for i in tri.vertices)
   counts[ob.name]=len(me.loop_triangles)
 ev.to_mesh_clear()
export=bpy.data.collections.new('Web export temporary');s.collection.children.link(export);exported=[]
for name,g in groups.items():
 me=bpy.data.meshes.new('WEB '+name);me.from_pydata(g['v'],[],g['f']);me.materials.append(g['m']);me.update()
 # Merge duplicated vertices for a compact GLB and consistent normals.
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.00003);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free()
 
 if 'upholstery' in name:
  for face in me.polygons:face.use_smooth=True
 ob=bpy.data.objects.new('WEB '+name,me);export.objects.link(ob);exported.append(ob)
bpy.ops.object.select_all(action='DESELECT')
for o in exported:o.select_set(True)
bpy.context.view_layer.objects.active=exported[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'ISEC.glb'),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_extras=False,export_yup=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
(OUT/'collision.json').write_text(json.dumps({'vertices':cv,'indices':ct},separators=(',',':')))
(ROOT/'renders/validation/export_report.json').write_text(json.dumps({'master_objects':len(original),'web_material_batches':len(exported),'visual_triangles':sum(len(g['f'])for g in groups.values()),'collision_triangles':len(ct)//3,'collision_objects':counts,'coordinate_transform':'Blender (x,y,z) -> web (x,z,-y)'},indent=2))
for o in exported:bpy.data.objects.remove(o,do_unlink=True)
bpy.data.collections.remove(export)
print('Exported',len(groups),'batches;',len(ct)//3,'collision triangles;',round((OUT/'ISEC.glb').stat().st_size/1048576,2),'MB')
