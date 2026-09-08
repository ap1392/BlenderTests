import sys,json
from pathlib import Path
sys.path.insert(0,'/private/tmp/isec_fidelity_deps')
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
root=Path(__file__).resolve().parents[3];d=json.loads((root/'references/fidelity/calibration/public_floor_union.json').read_text());ps=[]
for part in d['parts']:
 rings=[[part['vertices'][i]for i in r]for r in part['rings']];ps.append(Polygon(rings[0],rings[1:]))
p=unary_union(ps).buffer(-.08).difference(Point(0,0).buffer(3.12,quad_segs=64));intervals=[]
for i in range(228):
 x=-24+i*.21;cut=p.intersection(LineString([(x,-30),(x,30)]))
 for l in getattr(cut,'geoms',[cut]):
  if l.geom_type=='LineString' and l.length>.03:intervals.append([x,l.bounds[1],l.bounds[3]])
parts=[]
for q in getattr(p,'geoms',[p]):
 if q.geom_type=='Polygon':parts.append([list(q.exterior.coords)[:-1]]+[list(r.coords)[:-1]for r in q.interiors])
(root/'references/fidelity/calibration/ceiling_intervals.json').write_text(json.dumps({'intervals':intervals,'parts':parts}));print(len(intervals),'clipped slat intervals')
