import sys,json
from pathlib import Path
sys.path.insert(0,'/private/tmp/isec_fidelity_deps')
from shapely.geometry import Polygon
from shapely.ops import unary_union,triangulate
root=Path(__file__).resolve().parents[3]
d=json.loads((root/'references/fidelity/calibration/ground_floor_union.json').read_text())
old=Polygon([d['vertices'][i]for i in d['rings'][0]],[[d['vertices'][i]for i in r]for r in d['rings'][1:]])
controls=[((x-806)*.1,(480-y)*.1)for x,y in [(650,330),(740,311),(837,297),(928,294),(1016,294)]]
def point(px):
 x=(px-806)*.1
 for a,b in zip(controls,controls[1:]):
  if a[0]<=x<=b[0]:return (x,a[1]+(x-a[0])/(b[0]-a[0])*(b[1]-a[1]))
rooms=[]
for a,d in [(656,732),(750,825),(845,922),(938,1014)]:
 pa,pb=point(a),point(d);dx=pb[0]-pa[0];dy=pb[1]-pa[1];ln=(dx*dx+dy*dy)**.5;n=(-dy/ln,dx/ln)
 rooms.append(Polygon([pa,pb,(pb[0]+n[0]*5.67,pb[1]+n[1]*5.67),(pa[0]+n[0]*5.67,pa[1]+n[1]*5.67)]).buffer(.08,join_style=2))
p=unary_union([old]+rooms).buffer(0)
assert p.geom_type=='Polygon'and p.is_valid
coords=[];faces=[];lookup={}
def idx(co):
 key=(round(co[0],7),round(co[1],7))
 if key not in lookup:lookup[key]=len(coords);coords.append(key)
 return lookup[key]
for t in triangulate(p):
 if p.covers(t.representative_point())and t.intersection(p).area/t.area>.99999:faces.append([idx(co)for co in list(t.exterior.coords)[:3]])
rings=[[idx(co)for co in list(r.coords)[:-1]]for r in [p.exterior]+list(p.interiors)]
(root/'references/fidelity/calibration/ground_floor_classroom_union.json').write_text(json.dumps({'vertices':coords,'triangles':faces,'rings':rings,'area':p.area,'added_area':p.area-old.area},indent=2))
print('Supported classroom floor extension area',p.area-old.area)
