"""Rebuild source material families as editable Unreal shaders for visual calibration."""
import unreal,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'unreal/source/materials';m=json.loads((SRC/'manifest.json').read_text())
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;report={'complete':False,'materials':[],'visual_calibration':'pending','shader_compile_checked':True}
textures={}
for image in m['images']:
 name='T_'+re.sub('[^A-Za-z0-9_]','_',Path(image['file']).stem)
 path='/Game/ISEC/Textures/'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  task=unreal.AssetImportTask();task.filename=str(SRC/image['file']);task.destination_path='/Game/ISEC/Textures';task.destination_name=name;task.automated=True;task.save=True
  T.import_asset_tasks([task])
 textures[image['name']]=unreal.EditorAssetLibrary.load_asset(path)
def expression(mat,cls,**props):
 n=L.create_material_expression(mat,getattr(unreal,cls))
 for k,v in props.items():n.set_editor_property(k,v)
 return n
def scalar(mat,v):return expression(mat,'MaterialExpressionConstant',r=float(v))
def vector(mat,v):return expression(mat,'MaterialExpressionConstant3Vector',constant=unreal.LinearColor(*v[:3],1))
def prop(node,p):L.connect_material_property(node,'',getattr(unreal.MaterialProperty,p))
def connect(a,b,p):
 names=[str(n)for n in L.get_material_expression_input_names(b)]
 actual=p
 if p not in names:
  matches=[n for n in names if re.sub('[^a-z]','',n.lower()).endswith(re.sub('[^a-z]','',p.lower()))]
  if len(matches)==1:actual=matches[0]
 if not L.connect_material_expressions(a,'',b,actual):raise RuntimeError(f'Cannot connect {p}; available inputs {names}')
for item in m['materials']:
 name=item['name'];label='M_'+re.sub('[^A-Za-z0-9_]','_',name)+'_'+hashlib.sha256(name.encode()).hexdigest()[:6]
 if name=='Clear architectural glazing':label+='_thin_v2'
 path='/Game/ISEC/Materials/'+label
 mat=unreal.EditorAssetLibrary.load_asset(path)if unreal.EditorAssetLibrary.does_asset_exist(path)else T.create_asset(label,'/Game/ISEC/Materials',unreal.Material,unreal.MaterialFactoryNew())
 if name=='Clear architectural glazing'and unreal.EditorAssetLibrary.get_metadata_tag(mat,'ISEC_ValidatedGlass')=='v2':
  compiler_errors=[str(e)for e in L.recompile_material(mat)]
  if compiler_errors:raise RuntimeError(str(compiler_errors))
  report['materials'].append({'source':name,'asset':mat.get_path_name(),'compiler_errors':[],'translation':'Validated thin-translucent shader; rendered calibration pending'})
  continue
 L.delete_all_material_expressions(mat)
 # The Blender master shades these architectural sheets from both sides.
 # Its continuous stair soffits have upward winding and no thickness; preserve
 # the visible underside without altering authoritative geometry.
 if name in {'Cinematic satin white architectural enamel','Warm white painted steel and plaster'}:
  mat.set_editor_property('two_sided',True)
 bs=next((n['inputs']for n in item['nodes']if n['type']=='ShaderNodeBsdfPrincipled'),{})
 color=bs.get('Base Color',item['diffuse_color_linear']);base=vector(mat,color)
 family=name.lower();texture=None
 if 'concrete'in family:texture=next(iter(textures.values()))
 if 'mural'in family:texture=textures['slide-6-7-1600x900.jpg']
 if texture:
  base=expression(mat,'MaterialExpressionTextureSample',texture=texture)
  if 'concrete' in family:
   # Retain the exact UV multiplier from Blender fidelity revision 42.
   # The earlier JSON socket dictionary lost duplicate "Vector" input names.
   uv=expression(mat,'MaterialExpressionTextureCoordinate',u_tiling=1/4.6,v_tiling=1/1.45)
   connect(uv,base,'UVs')
 elif any(s in family for s in ['oak','carpet','upholstery','cloth','textile','terrazzo']):
  uv=expression(mat,'MaterialExpressionTextureCoordinate')
  uv3=expression(mat,'MaterialExpressionAppendVector');connect(uv,uv3,'A');connect(scalar(mat,0),uv3,'B')
  scale=vector(mat,([1.1,180,1] if name=='Light rift cut white oak' else [3,95,1])if'oak'in family else[130,130,1])
  mul=expression(mat,'MaterialExpressionMultiply');connect(uv3,mul,'A');connect(scale,mul,'B')
  fabric=any(word in family for word in ['upholstery','cloth','textile'])
  noise=expression(mat,'MaterialExpressionNoise',scale=1.0,levels=3,quality=2,output_min=.97 if fabric else .86,output_max=1.015 if fabric else 1.04)
  connect(mul,noise,'Position');variation=expression(mat,'MaterialExpressionMultiply');connect(base,variation,'A');connect(noise,variation,'B');base=variation
 prop(base,'MP_BASE_COLOR');prop(scalar(mat,bs.get('Roughness',.5)),'MP_ROUGHNESS');prop(scalar(mat,bs.get('Metallic',0)),'MP_METALLIC')
 emission=bs.get('Emission Strength',0)
 # Blender radiance values do not transfer as apparent brightness under this
 # Unreal exposure. Calibrate the visible diffuser/LED luminance explicitly.
 emission={'Warm white diffuser':600,'Stair warm concealed LED':1000,'Exit sign red':100}.get(name,emission)
 if emission:
  c=bs.get('Emission Color',[1,1,1]);prop(vector(mat,[v*emission for v in c[:3]]),'MP_EMISSIVE_COLOR')
 if name=='Clear architectural glazing':
  mat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT)
  mat.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_THIN_TRANSLUCENT)
  mat.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
  mat.set_editor_property('two_sided',True)
  output=expression(mat,'MaterialExpressionThinTranslucentMaterialOutput');connect(vector(mat,[.992,.998,1]),output,'TransmittanceColor')
  prop(scalar(mat,.025),'MP_OPACITY')
 L.layout_material_expressions(mat)
 compiler_errors=[str(e)for e in L.recompile_material(mat)]
 if compiler_errors:
  report['compiler_error']={'material':name,'errors':compiler_errors}
  (ROOT/'unreal/validation/material_build.json').write_text(json.dumps(report,indent=2))
  raise RuntimeError('Material compile failed: '+name+': '+str(compiler_errors))
 unreal.EditorAssetLibrary.save_loaded_asset(mat)
 if name=='Clear architectural glazing':
  unreal.EditorAssetLibrary.set_metadata_tag(mat,'ISEC_ValidatedGlass','v2');unreal.EditorAssetLibrary.save_loaded_asset(mat)
 report['materials'].append({'source':name,'asset':mat.get_path_name(),'compiler_errors':[],'translation':'Image texture or rebuilt procedural material; requires rendered calibration'})
 (ROOT/'unreal/validation/material_build.json').write_text(json.dumps(report,indent=2))
report['complete']=True;(ROOT/'unreal/validation/material_build.json').write_text(json.dumps(report,indent=2))
