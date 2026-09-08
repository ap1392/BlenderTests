"""Run with bundled Python, not Blender. Build reliable 2D polygons and triangulation."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,'/private/tmp/isec_fidelity_deps')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union,triangulate
root=Path(__file__).resolve().parents[3];data=json.loads((root/'references/fidelity/calibration/current_floor_geometry.json').read_text())
polys=[LineString(data['south']).buffer(-3.4,single_sided=True,join_style='round',cap_style='flat',quad_segs=16)]
checks=[]
for ob in data['objects']:
 if 'carpet'not in ob['name']or ob['name']in ['L2 carpet finish','L2 write-up carpet']:continue
 pts=[v[:2]for v in ob['vertices']if abs(v[2]-ob['z'])<1e-4];p=Polygon(pts);checks.append({'name':ob['name'],'valid':p.is_valid,'area':p.area});polys.append(p.buffer(0))
north=data['north'];south=data['south'];polys.append(Polygon([north[0],south[0],(south[0][0]-3,south[0][1]),(north[0][0]-3,north[0][1])]))
polys.append(Polygon([south[0],(-20.9,-.7),(-18.4257,-4.1)]))
a=math.radians(-47);polys.append(Polygon([(1.48*math.cos(a),1.48*math.sin(a)),(3*math.cos(a),3*math.sin(a)),(3.5,-3.4),(1.7,-4.4)]))
combined=unary_union(polys).buffer(0)
# Sub-millimetre topological snapping avoids tiny gaps between coplanar source panels.
combined=combined.buffer(.0004,join_style='mitre').buffer(-.0004,join_style='mitre')
parts=list(combined.geoms)if combined.geom_type=='MultiPolygon'else[combined]
result=[]
for p in parts:
 coords=[];faces=[];lookup={}
 def idx(co):
  key=(round(co[0],7),round(co[1],7))
  if key not in lookup:lookup[key]=len(coords);coords.append(key)
  return lookup[key]
 for t in triangulate(p):
  if p.covers(t.representative_point())and t.intersection(p).area/t.area>.99999:faces.append([idx(co)for co in list(t.exterior.coords)[:3]])
 rings=[[idx(co)for co in list(r.coords)[:-1]]for r in [p.exterior]+list(p.interiors)]
 result.append({'vertices':coords,'triangles':faces,'rings':rings,'area':p.area})
(root/'references/fidelity/calibration/public_floor_union.json').write_text(json.dumps({'parts':result,'checks':checks,'area':combined.area,'valid':combined.is_valid},indent=2))
print('Valid:',combined.is_valid,'parts:',len(parts),'area:',combined.area,'source checks:',checks)
