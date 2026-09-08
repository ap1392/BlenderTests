"""Run the shared batch exporter synchronously in Blender background mode."""
import bpy,json
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
smoke=json.loads((ROOT/'unreal/validation/smoke_import.json').read_text())
if not smoke.get('status','').startswith('imported;100cm cube verified'):
    raise RuntimeError('Unreal calibration must pass before the full export')
namespace={'__name__':'__main__','ISEC_UV_REPAIR_ONLY':globals().get('ISEC_UV_REPAIR_ONLY',False)}
p=ROOT/'blender/scripts/fidelity/71_export_architecture_batches.py'
exec(compile(p.read_text(),str(p),'exec'),namespace)
callback=namespace['next_group']
bpy.app.timers.unregister(callback)
while callback()is not None:pass
if namespace.get('export_failed'):raise RuntimeError('Batch export failed; see architecture/error.txt')
manifest=ROOT/'unreal/source/architecture/manifest.json'
if not manifest.exists():raise RuntimeError('Batch export did not complete; see architecture/error.txt')
print('ISEC_ARCHITECTURE_EXPORT_COMPLETE',flush=True)
