exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Initial camera registrations, refined against reference images in subsequent passes.
# Explicit source aspect ratios prevent letterboxing-induced focal errors.
cameras=[
 ('REF02_Reverse_soffit',(-2,-2,H+1.65),(13,10,H+1.3),20,1098,900,.0,'references/fidelity/visual/crop_slide-7-6-1600x900.jpg'),
 ('REF03_Social_hub',(-7,-8.4,2*H+1.6),(1,0,2*H+1.6),20,1258,900,.05,'references/fidelity/visual/crop_slide-6-7-1600x900.jpg'),
 ('REF04_Writeup',(14,15,H+1.6),(-14,11,H+1.6),19,1600,772,0,'references/fidelity/visual/crop_slide-8-3-1600x900.jpg'),
 ('REF05_Lower_stair',(8.9,8.9,1.6),(4.0,1.6,3.5),28,467,700,0,'references/fidelity/stair/wausau2.jpeg'),
 ('REF06_Upper_reverse',(-18,4,3*H+1.6),(5,0,11),19,467,700,0,'references/fidelity/stair/wausau3.jpeg'),
 ('REF07_Stair_elevation',(9,1,3*H+1.6),(0,0,3*H+1.6),29,467,700,0,'references/fidelity/stair/wausau4.jpeg'),
 ('REF08_Stair_overhead',(1.9,-2,4*H+1.6),(0,0,2*H),23,467,700,0,'references/fidelity/stair/wausau1.jpeg'),
 ('REF09_Ground_wide',(16,8,1.4),(-2,4,6.6),17,1917,1279,0,'references/fidelity/atrium/isec_reflections_011.jpg'),
 ('REF10_Glass_elevation',(2,-4,3*H+1.6),(2,11,3*H+1.6),27,1923,1280,0,'references/fidelity/atrium/isec_reflections_018.jpg'),
 ('REF11_End_bridge',(14,3,2*H+1.6),(21.5,11,2*H+2.4),22,1923,1280,0,'references/fidelity/atrium/isec_reflections_023.jpg'),
 ('REF12_Roof_reverse',(-17,4,4*H+1.6),(6,3,17.5),15,1400,934,0,'references/fidelity/atrium/neu_m0413673f.jpg')]
for name,loc,target,lens,w,h,shift,ref in cameras:
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 ob=bpy.data.objects.new(name,bpy.data.cameras.new(name));COL['Cameras'].objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens;ob.data.shift_y=shift;ob.data.clip_end=300;ob['reference']=ref;ob['render_width']=w;ob['render_height']=h;ob['registration']='INITIAL perspective seed; awaiting rendered comparison'
cam=bpy.data.objects['REF01_Payette_atrium'];cam['render_width']=1149;cam['render_height']=900;cam['registration']='Near stair foot and far bridge landmark fit, manual correspondences'
(ROOT/'references/fidelity/calibration/camera_register.json').write_text(json.dumps([{'camera':o.name,'location':list(o.location),'lens_mm':o.data.lens,'reference':o.get('reference'),'status':o.get('registration')}for o in COL['Cameras'].objects if o.name.startswith('REF')],indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('12 reference cameras saved')
