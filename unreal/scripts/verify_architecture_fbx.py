"""Independently check every exported FBX's vertex count and source bounds."""
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
# Reuse just the pure parser function, without executing the smoke validator.
src=ROOT/'unreal/scripts/verify_fbx_smoke.py'
tree=ast.parse(src.read_text())
parser=ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[])
ns={};exec(compile(parser,str(src),'exec'),ns)
p=ROOT/'unreal/source/architecture';m=json.loads((p/'manifest.json').read_text());rows=[]
for a in m['batches']:
 version,arrays=ns['read_arrays'](p/a['file']);errors=[]
 if len(arrays)!=1:errors.append('Expected exactly one geometry')
 v=arrays[0]if arrays else[]
 if len(v)!=a['vertices']*3:errors.append('Vertex count mismatch')
 if v:
  for k,fn in [('min',min),('max',max)]:
   if any(abs(fn(v[j::3])-a['bounds_m'][k][j])>1e-4 for j in range(3)):errors.append('Bounds mismatch: '+k)
 rows.append({'asset':a['asset'],'vertices':len(v)//3,'errors':errors})
r={'passed':bool(rows)and all(not x['errors']for x in rows),'batches':len(rows),'vertices':sum(x['vertices']for x in rows),'results':rows}
(p/'file_validation.json').write_text(json.dumps(r,indent=2))
print({k:v for k,v in r.items()if k!='results'})
if not r['passed']:raise SystemExit(1)
