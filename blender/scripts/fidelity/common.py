"""Selective refinement helpers; loads existing scene without reconstructing it."""
import bpy, math, json, random, ast
from pathlib import Path
from mathutils import Vector, Matrix
from math import sin,cos,pi
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
DETAIL=True
COL={c.name:c for c in bpy.data.collections}
C='Architecture'
# Reuse geometry utilities without executing original destructive build body.
tree=ast.parse((ROOT/'blender/scripts/build_isec.py').read_text())
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['put','mesh','box','beam','poly','smooth','offset','strip','ribbon','rail','mat']]
exec(compile(ast.Module(body=funcs,type_ignores=[]),'existing_geometry_helpers','exec'))
def material(prefix):return next(m for m in bpy.data.materials if m.name.startswith(prefix))
white=bpy.data.materials['Warm white painted steel and plaster'];floor=material('Pale grey');concrete=material('Board formed');metal=material('Brushed stainless');dark=material('Charcoal mullions');glass=material('Clear architectural');spandrel=material('Blue grey');wood=material('Natural oak');carpet=material('Charcoal carpet');lime=material('Social hub');pink=material('Magenta');blue=material('Petrol');yellow=material('Chartreuse');black=material('Ceiling acoustic');em=material('Warm white diffuser')
P=lambda pts:[((x-806)*.10,(480-y)*.10)for x,y in pts]
north=smooth(P([(605,409),(700,382),(800,365),(900,357),(994,357)]),10)
south=smooth(P([(627,487),(663,494),(700,514),(730,547),(740,557),(790,530),(870,485),(945,444),(990,420),(994,398),(994,357)]),6)
H=4.4196;FLOORS=[i*H for i in range(6)];ROOF=6*H

def remove_where(test):
 objs=[o for o in bpy.data.objects if test(o)]
 bpy.data.batch_remove(objs)

def finish(o,smooth_sides=False):
 import bmesh
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
 if smooth_sides:
  for f in bm.faces:f.smooth=True
  for e in bm.edges:
   if len(e.link_faces)==2 and e.calc_face_angle()>.55:e.smooth=False
 bm.to_mesh(o.data);bm.free();return o

def curve_tube(name,points,radius,ma):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=radius;cu.bevel_resolution=3
 sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cu);COL[C].objects.link(ob);cu.materials.append(ma);return ob

def path_resample(path,n):
 p=[Vector(v) for v in path];cum=[0]
 for a,b in zip(p,p[1:]):cum.append(cum[-1]+(b-a).length)
 out=[]
 for j in range(n):
  d=cum[-1]*j/(n-1);i=next((i for i in range(1,len(cum)) if cum[i]>=d),len(cum)-1);t=(d-cum[i-1])/max(1e-9,cum[i]-cum[i-1]);out.append(tuple(p[i-1].lerp(p[i],t)))
 return out

def panel_glass(name,path,zbase,ztop):
 o=ribbon(name,path,[zbase]*len(path),ztop-zbase,.012,glass,False);finish(o);return o
