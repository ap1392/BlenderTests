import sys,json
from pathlib import Path
sys.path.insert(0,'/private/tmp/isec_fidelity_deps')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union,triangulate
root=Path(__file__).resolve().parents[3];base=root/'references/fidelity/calibration';data=json.loads((base/'public_floor_union.json').read_text());wall=json.loads((base/'terrace_wall_trace.json').read_text());P=lambda pts:[((x-806)*.1,(480-y)*.1)for x,y in pts]
inner=P([(740,562),(732,538),(713,511),(680,494),(649,487),(627,487)])
inset=[]
for i,p in enumerate(wall):
 a=wall[max(0,i-1)];b=wall[min(len(wall)-1,i+1)];dx=b[0]-a[0];dy=b[1]-a[1];length=(dx*dx+dy*dy)**.5;inset.append((p[0]+.20*dy/length,p[1]-.20*dx/length))
outline=[(-19.1,2.7),(-16.6,3.0)]+inset+inner
terrace=Polygon(outline).buffer(0);parts=[]
for p in data['parts']:
 rr=[[p['vertices'][i]for i in r]for r in p['rings']];parts.append(Polygon(rr[0],rr[1:]))
joined=unary_union(parts+[terrace]).buffer(.001).buffer(-.001)
def mesh(p):
 vs=[];lookup={};faces=[]
 def idx(co):
  k=tuple(round(a,7)for a in co)
  if k not in lookup:lookup[k]=len(vs);vs.append(k)
  return lookup[k]
 for t in triangulate(p):
  if p.covers(t.representative_point())and t.intersection(p).area/t.area>.99999:faces.append([idx(co)for co in list(t.exterior.coords)[:3]])
 rings=[[idx(co)for co in list(r.coords)[:-1]]for r in [p.exterior]+list(p.interiors)]
 return {'vertices':vs,'triangles':faces,'rings':rings}
line=json.loads((base/'current_floor_geometry.json').read_text())['south'];line=[p for p in line if p[0]<1.35];g=LineString(line).difference(terrace.buffer(.03));guards=[list(x.coords)for x in getattr(g,'geoms',[g])if x.geom_type=='LineString'and x.length>.25]
out={'floor':mesh(joined),'terrace':mesh(terrace),'guards':guards,'outer':outline[:2]+wall,'inner':inner,'area':terrace.area};(base/'l2_terrace_union.json').write_text(json.dumps(out));print('L2 floor',joined.geom_type,'terrace area',terrace.area,'remaining guard spans',len(guards))
