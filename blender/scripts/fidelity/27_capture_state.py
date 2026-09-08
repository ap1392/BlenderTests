"""Snapshot current calibrated cameras and pack refinement records. Does not rebuild geometry."""
import bpy,json
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
cam=bpy.data.objects['REF01_Payette_atrium'];cam['reference']='references/fidelity/calibration/atrium-slide-10-1600x900.jpg'
bpy.data.objects['REF08_Stair_overhead']['reference']='references/fidelity/atrium/isec_reflections_004-1.jpg'
records=[]
for ob in sorted([o for o in bpy.data.objects if o.type=='CAMERA'and o.name.startswith('REF')],key=lambda o:o.name):
 ob['registration']='Iteratively reference compared. EXIF focal length where available; positions, crop and shift approximate.'
 records.append({'camera':ob.name,'location':list(ob.location),'rotation_euler':list(ob.rotation_euler),'projection':ob.data.type,'lens_mm':ob.data.lens,'sensor_width_mm':ob.data.sensor_width,'sensor_height_mm':ob.data.sensor_height,'photographic_exposure':ob.get('photographic_exposure',.7),'crop_note':ob.get('crop_estimate'),'source_exif_focal_mm':ob.get('source_exif_focal_length_mm'),'fisheye_lens':ob.data.fisheye_lens if ob.data.type=='PANO'else None,'shift_x':ob.data.shift_x,'shift_y':ob.data.shift_y,'clip_start':ob.data.clip_start,'reference':ob.get('reference'),'render_width':ob.get('render_width'),'render_height':ob.get('render_height'),'status':ob['registration']})
(root/'references/fidelity/calibration/camera_register.json').write_text(json.dumps(records,indent=2))
# Exploratory cameras remain recorded in prior scripts/renders; the master exposes12 matched views.
bpy.data.batch_remove([o for o in bpy.data.objects if o.type=='CAMERA'and o.name.startswith('TEST02_')])
for p in sorted((root/'blender/scripts/fidelity').glob('*.py')):
 name='fidelity/'+p.name;text=bpy.data.texts.get(name)or bpy.data.texts.new(name);text.clear();text.write(p.read_text())
for relative in ['references/fidelity/iteration_register.md','references/remaining_fidelity_work.md','references/fidelity/calibration/camera_register.json','references/fidelity/camera_discrepancies.md','references/assumptions_and_uncertainties.txt','references/reference_sources.txt','references/fidelity/current_pass_report.md','references/fidelity/calibration/integrity_audit.json','references/fidelity/calibration/fixture_clearance_audit.json']:
 p=root/relative;t=bpy.data.texts.get(relative)or bpy.data.texts.new(relative);t.clear();t.write(p.read_text())
bpy.ops.file.pack_all()
s=bpy.context.scene;s.cycles.max_bounces=12;s.cycles.diffuse_bounces=6;s.cycles.glossy_bounces=6;s.cycles.transmission_bounces=12
s.camera=bpy.data.objects['REF01_Payette_atrium'];s.render.resolution_x=1149;s.render.resolution_y=900;s.view_settings.exposure=s.camera.get('photographic_exposure',.7)
s['fidelity_status']='Substantial reference-driven refinement;12comparison cameras; geometry, materials and framing retain documented uncertainty. Not an as-built survey.'
bpy.ops.wm.save_as_mainfile(filepath=str(root/'blender/ISEC_Master.blend'))
print('Camera state exported; refinement scripts and notes packed; master saved')
