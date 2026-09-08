"""Independent binary-FBX geometry check against the Blender smoke manifest.

This checks the files actually written, not merely the export operator result.
It does not replace the required Unreal unit/orientation/material roundtrip.
"""
import json,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'unreal/source/smoke'

def read_arrays(path):
    data=path.read_bytes()
    if not data.startswith(b'Kaydara FBX Binary'):raise ValueError('Not binary FBX')
    version=struct.unpack_from('<I',data,23)[0]
    header,fmt=(25,'<QQQB')if version>=7500 else(13,'<IIIB')
    arrays=[]
    def node(offset,parent=''):
        end,count,length,name_length=struct.unpack_from(fmt,data,offset)
        if not end:return len(data)
        start=offset+header
        name=data[start:start+name_length].decode(errors='replace')
        p=start+name_length
        if name=='Vertices':
            kind=chr(data[p]);size,encoding,byte_count=struct.unpack_from('<III',data,p+1)
            if kind not in 'df':raise ValueError('Unexpected vertex type '+kind)
            raw=data[p+13:p+13+byte_count]
            if encoding==1:raw=zlib.decompress(raw)
            elif encoding!=0:raise ValueError('Unknown array encoding')
            arrays.append(struct.unpack('<'+str(size)+kind,raw))
        p+=length
        while p+header<=end and any(data[p:p+header]):p=node(p,name)
        return end
    p=27
    while p+header<len(data) and any(data[p:p+header]):p=node(p)
    return version,arrays

manifest=json.loads((FOLDER/'manifest.json').read_text());results=[]
for asset in manifest['assets']:
    version,arrays=read_arrays(FOLDER/asset['file'])
    errors=[]
    if len(arrays)!=1:errors.append(f'Expected one geometry, got{len(arrays)}')
    points=arrays[0]if arrays else[]
    if len(points)!=3*asset['vertices']:errors.append(f'Expected{asset["vertices"]}vertices, got{len(points)//3}')
    actual={}
    if points:
        actual={'min_m':[min(points[j::3])for j in range(3)],'max_m':[max(points[j::3])for j in range(3)]}
        for key in actual:
            if any(abs(a-b)>1e-4 for a,b in zip(actual[key],asset['bounds'][key])):
                errors.append('Source-coordinate bounds mismatch: '+key)
    results.append({'asset':asset['id'],'fbx_version':version,'bytes':(FOLDER/asset['file']).stat().st_size,
                    'vertices':len(points)//3,'bounds':actual,'errors':errors})
report={'passed':all(not r['errors']for r in results),
        'scope':'Binary vertex arrays and source-coordinate bounds only. Unreal import has not run.',
        'assets':results}
(FOLDER/'file_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not report['passed']:raise SystemExit(1)
