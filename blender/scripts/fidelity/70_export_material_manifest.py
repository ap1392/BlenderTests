"""Archive material nodes and packed source images for a deliberate UE rebuild."""
import bpy,json,hashlib,re
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
OUT=ROOT/'unreal/source/materials';OUT.mkdir(parents=True,exist_ok=True)
TEX=OUT/'textures';TEX.mkdir(exist_ok=True)
def value(v):
    if v is None or isinstance(v,(str,int,float,bool)):return v
    try:return list(v)
    except TypeError:return str(v)
images={};materials=[]
for mat in bpy.data.materials:
    if not mat.users:continue
    nodes=[];links=[]
    if mat.use_nodes:
        for n in mat.node_tree.nodes:
            r={'name':n.name,'type':n.bl_idname,'label':n.label,
               'inputs':{s.name:value(s.default_value)for s in n.inputs if hasattr(s,'default_value')},
               'properties':{p:value(getattr(n,p))for p in ['operation','blend_type','noise_dimensions','wave_type','bands_direction','wave_profile','distribution','feature','projection','extension']if hasattr(n,p)}}
            if hasattr(n,'color_ramp'):
                r['color_ramp']={'interpolation':n.color_ramp.interpolation,'elements':[{'position':e.position,'color':list(e.color)}for e in n.color_ramp.elements]}
            if n.type=='TEX_IMAGE' and n.image:
                img=n.image;r['image']=img.name
                if img.name not in images:
                    rec={'name':img.name,'source_path':img.filepath,'color_space':img.colorspace_settings.name,'size':list(img.size)}
                    if img.packed_file:
                        data=bytes(img.packed_file.data);digest=hashlib.sha256(data).hexdigest()
                        suffix='.png'if data.startswith(b'\x89PNG')else('.jpg'if data.startswith(b'\xff\xd8')else'.bin')
                        fn=re.sub('[^A-Za-z0-9_-]+','_',Path(img.name).stem)+'_'+digest[:10]+suffix
                        (TEX/fn).write_bytes(data);rec.update({'file':'textures/'+fn,'sha256':digest})
                    images[img.name]=rec
            nodes.append(r)
        links=[{'from_node':l.from_node.name,'from_socket':l.from_socket.name,'to_node':l.to_node.name,'to_socket':l.to_socket.name}for l in mat.node_tree.links]
    materials.append({'name':mat.name,'users':mat.users,'diffuse_color_linear':list(mat.diffuse_color),
                      'nodes':nodes,'links':links})
(OUT/'manifest.json').write_text(json.dumps({'status':'source archive; UE shaders must be rebuilt and visually validated',
    'color_note':'Blender color socket values are scene-linear; image color spaces recorded separately.',
    'provenance_note':'The board-formed concrete bitmap is an AI reconstruction. Mural content is a partial reference photograph crop. This archive does not change either provenance.',
    'materials':materials,'images':list(images.values())},indent=2))
print('Archived',len(materials),'materials and',len(images),'image references without modifying Blender materials')
