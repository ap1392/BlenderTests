exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
from bpy_extras.object_utils import world_to_camera_view
s=bpy.context.scene
# Fit two photographed vertical anchors, preserving actual65mm EXIF and ground eyeheight.
cam=bpy.data.objects['REF05_Lower_stair'];s.render.resolution_x=467;s.render.resolution_y=700
first=bpy.data.objects['Fidelity lower stair tread 00'];last=bpy.data.objects['Fidelity lower stair tread 29'];foot=first.matrix_world@((first.data.vertices[4].co+first.data.vertices[5].co)/2);top=last.matrix_world@((last.data.vertices[6].co+last.data.vertices[7].co)/2)
target=Vector((3.6,.6,2.8));direction=Vector((14.5-3.6,15.4-.6,0)).normalized()
def evaluate(dist,shift):
 cam.location=(target.x+direction.x*dist,target.y+direction.y*dist,1.55);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.shift_y=shift;bpy.context.view_layer.update()
 return[1-world_to_camera_view(s,cam,p).y for p in [foot,top]]
dist=18.38;shift=-.065;goal=[.895,.33]
for _ in range(8):
 f=evaluate(dist,shift);a=evaluate(dist+.01,shift);b=evaluate(dist,shift+.001);j00=(a[0]-f[0])/.01;j10=(a[1]-f[1])/.01;j01=(b[0]-f[0])/.001;j11=(b[1]-f[1])/.001;det=j00*j11-j01*j10
 if abs(det)<1e-8:break
 e0=goal[0]-f[0];e1=goal[1]-f[1];dist+=max(-2,min(2,(e0*j11-e1*j01)/det));shift+=max(-.2,min(.2,(j00*e1-j10*e0)/det))
fit=evaluate(dist,shift);cam['vertical_anchor_fit']=str({'foot':fit[0],'top':fit[1],'distance':dist,'shift':shift,'source_anchors_approximate':True})
# Source58mm stair image can be photographed close to the laboratory glass, avoiding desks.
def camera(name,loc,target,lens):
 ob=bpy.data.objects[name];ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens
camera('REF07_Stair_elevation',(16.2,12.4,3*H+1.65),(0,0,3*H+.65),58)
# Central southern gallery is deep enough for the source35mm elevation sightline.
camera('REF10_Glass_elevation',(6,-4.3,3*H+1.65),(6,12.2,3*H+1.65),35)
# The Payette image has vertical framing shift; retain the clearer lowerstair-side seed.
base=bpy.data.objects['TEST02_5'];cam=bpy.data.objects['REF02_Reverse_soffit'];cam.location=base.location;cam.rotation_euler=base.rotation_euler;cam.data.shift_y=.15
# University roof photograph has pronounced fisheye curvature; no reliable focalEXIF.
cam=bpy.data.objects['REF12_Roof_reverse'];cam.data.type='PANO';cam.data.panorama_type='FISHEYE_EQUISOLID';cam.data.fisheye_lens=15.3;cam.data.fisheye_fov=pi;cam['projection_note']='Full-frame equisolid fisheye approximation. SourceNikonD810EXIF has unreported manual-lens focal length.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('65mm vertical fit',fit,'distance',dist,'shift',shift)
