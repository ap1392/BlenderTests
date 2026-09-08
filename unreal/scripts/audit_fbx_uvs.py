"""Check triangulated FBX face UV areas to catch collapsed UV charts before Unreal."""
import json,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def arrays(path):
 data=path.read_bytes();version=struct.unpack_from('<I',data,23)[0];header,fmt=(25,'<QQQB')if version>=7500 else(13,'<IIIB');out={}
 def node(offset):
  end,count,length,n=struct.unpack_from(fmt,data,offset)
  if not end:return len(data)
  start=offset+header;name=data[start:start+n].decode(errors='replace');p=start+n
  if name in ['Vertices','PolygonVertexIndex','UV','UVIndex','Normals','NormalsIndex']:
   kind=chr(data[p]);size,encoding,byte_count=struct.unpack_from('<III',data,p+1);raw=data[p+13:p+13+byte_count]
   if encoding==1:raw=zlib.decompress(raw)
   out.setdefault(name,[]).append(struct.unpack('<'+str(size)+kind,raw))
  p+=length
  while p+header<=end and any(data[p:p+header]):p=node(p)
  return end
 p=27
 while p+header<len(data)and any(data[p:p+header]):p=node(p)
 return out
def audit(path):
 a=arrays(path);uv=a['UV'][0];idx=a.get('UVIndex',[None])[0];pv=a['PolygonVertexIndex'][0];poly=[];bad=0;total=0
 for j,v in enumerate(pv):
  k=idx[j]if idx else j;poly.append((uv[2*k],uv[2*k+1]))
  if v<0:
   area=abs(sum(poly[n][0]*poly[(n+1)%len(poly)][1]-poly[(n+1)%len(poly)][0]*poly[n][1]for n in range(len(poly))))
   bad+=area<1e-12;total+=1;poly=[]
 normals=a.get('Normals',[[]])[0]
 zero=sum(sum(x*x for x in normals[j:j+3])<1e-8 for j in range(0,len(normals),3))
 return {'file':path.name,'faces':total,'collapsed_uv_faces':bad,'zero_normals':zero}
if __name__=='__main__':
 import sys
 p=ROOT/'unreal/source/architecture';paths=[p/sys.argv[1]]if len(sys.argv)>1 else sorted(p.glob('*.fbx'))
 rows=[audit(f)for f in paths];r={'passed':all(x['collapsed_uv_faces']==0 and x['zero_normals']==0 for x in rows),'files':len(rows),'collapsed_uv_faces':sum(x['collapsed_uv_faces']for x in rows),'zero_normals':sum(x['zero_normals']for x in rows),'results':rows}
 if len(sys.argv)==1:(p/'uv_validation.json').write_text(json.dumps(r,indent=2))
 print(json.dumps({k:v for k,v in r.items()if k!='results'},indent=2))
 if not r['passed']:print([x for x in rows if x['collapsed_uv_faces']or x['zero_normals']])
