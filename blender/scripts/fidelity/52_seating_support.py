exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
import re
count=0
for ob in bpy.data.objects:
 if ob.get('seating_support_v52'):continue
 match=re.match(r'Gallery magenta bucket (\d+) ',ob.name)
 table=re.match(r'Gallery circular study table (\d+) ',ob.name)
 shift=None
 if match:
  group=int(match.group(1))%12
  if group<3:shift=(.33,-.63)
  elif group<6:shift=(0,-.20)
 elif table:
  group=int(table.group(1))%4
  if group==0:shift=(.33,-.63)
  elif group==1:shift=(0,-.20)
 if shift:
  ob.location.x+=shift[0];ob.location.y+=shift[1];ob['seating_support_v52']=True;count+=1
bpy.context.scene['seating_support_v52']='Moved complete social table/chair groups inward after exact floor-union support audit; first group shifted (+0.33,-0.63), second (0,-0.20). Preserves group layout while clearing the gallery boundary.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Moved complete supported seating groups:',count,'parts')
