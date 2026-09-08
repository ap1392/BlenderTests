exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith(('L1-L2 lower stair','Lower stair','Board formed concrete stair enclosure','Concrete board-form joint','West broad stair','L2 broad stair top landing','Collision lower stair','Collision broad stair')))
C='Staircase'
# Digitized northeast approach. Hidden upper continuation constrained by the L2 connection.
center=smooth(P([(875.6,428.5),(870,441),(860,457),(847,472),(835,484),(825,494),(819,503),(819,510)]),10)
center=path_resample(center,31);left=offset(center,.96);right=offset(center,-.96);heights=[H*i/30 for i in range(31)]
traction=bpy.data.materials.get('Stair charcoal abrasive')
for j in range(30):
 h=heights[j+1];pts=[left[j],right[j],right[j+1],left[j+1]];finish(poly(f'Fidelity lower stair tread {j:02}',pts,h,.07,floor))
 for dd in [.07,.14,.21]:
  a=Vector(left[j]).lerp(Vector(left[j+1]),dd);b=Vector(right[j]).lerp(Vector(right[j+1]),dd)
  curve_tube('Lower stair traction',[(*a,h+.002),(*b,h+.002)],.004,traction)
# Continuous loft across the tread-bearing shell.
fine=path_resample(smooth(center,4),181);ll=offset(fine,.98);rr=offset(fine,-.98);hh=[H*i/180 for i in range(181)]
v=[(*p,z-.18)for p,q,z in zip(ll,rr,hh)for p in [p,q]]
finish(mesh('Lower stair continuous soffit',v,[(i,i+2,i+3,i+1)for i in range(0,len(v)-2,2)],white),True)
for side in [ll,rr]:
 finish(ribbon('Lower stair continuous sidewall',side,[z-.24 for z in hh],.57,.06,white),True)
 for j in range(0,180,6):finish(ribbon('Lower stair clear glass panel',side[j:j+7],[z+.34 for z in hh[j:j+7]],.85,.013,glass,False),True)
 curve_tube('Lower stair inset handrail',[(*p,z+1.02)for p,z in zip(side,hh)],.021,metal)
 curve_tube('Lower stair recessed warm light',[(*p,z+.13)for p,z in zip(side,hh)],.007,bpy.data.materials['Stair warm concealed LED'])
# Open, hooked wall from high-resolution L1 plan; not a filled core.
C='Atrium';trace=json.loads((ROOT/'references/fidelity/stair/lower_stair_trace.json').read_text())['traces']
wall=smooth(P(trace['concrete_wall_outer_visible']),4)
finish(ribbon('Traced J concrete enclosure wall',wall,[0]*len(wall),H+.95,.26,concrete),True)
# Return over a visible recess, its lower part is open in Wausau front stair photo.
ret=smooth(P([(811.7,492.8),(816.9,477.8),(835.1,473.8)]),10)
finish(ribbon('Concrete wall above wood-lined recess',ret,[2.55]*len(ret),H+.95-2.55,.26,concrete),True)
C='Rooms';recess=P([(808,492),(812,478),(831,473)])
ribbon('Closed wood-lined recess wall',recess,[0]*len(recess),2.56,.12,wood)
# Broad stair between auditorium and labwing: traced east-to-west, with central pause.
C='Staircase';a=Vector(P([(704,429)])[0]);b=Vector(P([(615,440)])[0]);d=(b-a).normalized();n=Vector((-d.y,d.x));length=(b-a).length
run=(length-1.25)/28
segments=[];dist=0;z=0
for j in range(29):
 landing=j==14;step=1.25 if landing else run;rise=0 if landing else H/28
 p=a+d*dist;q=a+d*(dist+step);width=2.8 if j<15 else 2.5
 pts=[tuple(p-n*width/2),tuple(p+n*width/2),tuple(q+n*width/2),tuple(q-n*width/2)]
 finish(poly('Corrected broad stair landing'if landing else f'Corrected broad stair tread {j}',pts,z+rise,.14,floor))
 dist+=step;z+=rise;segments.append((dist,z))
for side in [-1,1]:
 pts=[tuple(a+n*1.4*side)]+[tuple(a+d*t+n*1.4*side)for t,z in segments];zz=[0]+[z for t,z in segments]
 ribbon('Broad stair glass guard',pts,[h+.08 for h in zz],1.08,.014,glass)
 curve_tube('Broad stair stainless rail',[(*p,h+1.0)for p,h in zip(pts,zz)],.021,metal)
poly('Broad stair west top connection',P([(605,424),(615,423),(620,451),(611,453)]),H,.25,white)
# Replace invented auditorium curve with later published boundary; room remains closed.
remove_where(lambda o:o.name.startswith('Closed auditorium curved boundary'))
C='Rooms';aud=smooth(P([(477,469),(550,456),(620,451),(680,450),(710,457),(735,477),(747,499)]),7)
finish(ribbon('Auditorium documented north and east boundary',aud,[0]*len(aud),H-.1,.24,white),True)
# Full undercroft floor and correct columns set behind the atrium glazing line.
C='Atrium';strip('Extended ground public undercroft',north,-7.5,0,.28,floor)
remove_where(lambda o:o.name.startswith(('Round atrium column','Ground classroom front wall','Ground undercroft end boundary','Closed classroom oak double door','Classroom door pull')))
C='Architecture'
colpath=path_resample(offset(north,-3.1),6)
for p in colpath[1:-1]:finish(beam('Undercroft round concrete column',(*p,0),(*p,H-.12),.28,white),True)
# Classroom front glazing at the plan-supported back of undercroft.
C='Rooms';back=path_resample(offset(north,-7.0),25)
for i in range(24):
 p,q=back[i:i+2]
 if i in [4,10,16,22]:ribbon('Classroom closed pale oak leaf',[p,q],[0,0],2.7,.09,wood)
 else:panel_glass('Classroom full-height glazing',[p,q],.03,3.05)
 beam('Classroom vertical metal frame',(*p,0),(*p,3.1),.024,metal)
ribbon('Classroom white header',back,[3.08]*len(back),H-3.08,.16,white)
# Deeper occupied classroom portion limited to observed tables and rows behind CLOSED glazing.
roomend=offset(north,-13.5);ribbon('Classroom rear closure',roomend,[0]*len(roomend),H-.1,.18,white)
strip('Classroom observed floor',offset(north,-7),-6.5,0,.18,floor)
# White air-distribution band under the interior curtain wall with circular jet outlets.
C='Architecture';ribbon('Undercroft white air distribution fascia',north,[H-.65]*len(north),.65,.26,white)
for p in path_resample(north,29):
 idx=min(range(len(north)),key=lambda i:(Vector(north[i])-Vector(p)).length);v=Vector(offset(north,-.25)[idx])-Vector(north[idx]);v.normalize()
 a=Vector((*p,H-.34));direction=Vector((v.x,v.y,0))
 finish(beam('Circular supply outlet rim',a-direction*.04,a+direction*.025,.091,white),True)
 finish(beam('Circular supply outlet recess',a-direction*.045,a-direction*.043,.063,dark),True)
# Existing ground furnishing is temporarily removed from conflicting zones, rebuilt after architecture.
for o in list(COL['Furniture'].objects):
 if o.type=='MESH' and o.location.z<.1 and (o.name.startswith(('Egg','Sculpted','Swivel','Four star','Bucket'))):o.hide_render=True
bpy.context.scene['fidelity_ground']='Lower approach and wall traced; hidden upper transition inferred; broad stair reoriented to plans; classroom closed glazed frontage restored'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Ground geometry refinement saved')
