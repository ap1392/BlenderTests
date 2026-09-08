import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
manifest=json.loads((ROOT/'unreal/source/cinematic_camera_manifest.json').read_text())
s=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get()
objects=[];trees={};issues=[]
for o in bpy.data.objects:
    if o.type not in {'MESH','CURVE'} or o.hide_render or o.name.lower().startswith('collision'):continue
    bb=[o.matrix_world@Vector(v) for v in o.bound_box]
    if not bb:continue
    objects.append((o,Vector(tuple(min(p[j] for p in bb)for j in range(3))),Vector(tuple(max(p[j] for p in bb)for j in range(3)))))
def tree_for(o):
    if o.name in trees:return trees[o.name]
    e=o.evaluated_get(deps);m=e.to_mesh();v=[o.matrix_world@x.co for x in m.vertices];f=[tuple(p.vertices)for p in m.polygons]
    tree=BVHTree.FromPolygons(v,f);e.to_mesh_clear();trees[o.name]=tree;return tree
for shot in manifest['shots']:
    for key in shot['keys']:
        p=Vector(key['location_m']);r=.15
        for o,lo,hi in objects:
            if any(p[j]<lo[j]-r or p[j]>hi[j]+r for j in range(3)):continue
            hit=tree_for(o).find_nearest(p)
            if hit and hit[0] is not None and hit[3]<r:
                issues.append({'shot':shot['name'],'frame':key['frame'],'object':o.name,'clearance_m':hit[3]})
report={'sampled_camera_positions':sum(len(x['keys'])for x in manifest['shots']),'camera_clearance_radius_m':.15,'surface_proximity_issues':issues,'evaluated_nearby_meshes':len(trees),'scope':'Camera center proximity to evaluated visible surfaces. Does not certify all frustum rays, path interiors or Unreal import; moving preview review also required.'}
(ROOT/'references/fidelity/calibration/cinematic_clearance.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
