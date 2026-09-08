import sys,json
from pathlib import Path
sys.path.insert(0,'/private/tmp/isec_fidelity_deps')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union,triangulate
root=Path(__file__).resolve().parents[3];d=json.loads((root/'references/fidelity/calibration/current_floor_geometry.json').read_text());north=d['north']
P=lambda pts:[((x-806)*.1,(480-y)*.1)for x,y in pts]
outline=P([(580,414)])+north+P([(1036,420),(1035,480),(1006,541),(954,588),(881,620),(793,641),(744,623),(750,571),(720,509),(680,465),(608,455)])
p=unary_union([Polygon(outline).buffer(0),LineString(north).buffer(13.5,single_sided=True,join_style='round',cap_style='flat')]).buffer(0)
assert p.geom_type=='Polygon'and p.is_valid
coords=[];faces=[];lookup={}
def idx(co):
 key=(round(co[0],7),round(co[1],7))
 if key not in lookup:lookup[key]=len(coords);coords.append(key)
 return lookup[key]
for t in triangulate(p):
 if p.covers(t.representative_point())and t.intersection(p).area/t.area>.99999:faces.append([idx(co)for co in list(t.exterior.coords)[:3]])
rings=[[idx(co)for co in list(r.coords)[:-1]]for r in [p.exterior]+list(p.interiors)]
(root/'references/fidelity/calibration/ground_floor_union.json').write_text(json.dumps({'vertices':coords,'triangles':faces,'rings':rings,'area':p.area},indent=2));print('Ground continuous polygon area',p.area)
