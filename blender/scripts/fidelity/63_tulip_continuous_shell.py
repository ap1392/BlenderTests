"""Continuous photo-derived tulip back/waist; replaces only the existing shared chair shell."""
exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
C='Furniture'
backs=[o for o in bpy.data.objects if o.name.startswith('Ground tall magenta tulip') and 'enveloping back' in o.name]
assert len(backs)==8
old=backs[0].data
N=96;M=72;verts=[]
# Smoothly connected foot, waist, seat-level flare and upper petal; no separate
# cylindrical pedestal seam. Shape is inferred from university011/022, not CAD.
profile=[(0.025,.34,.26,0),(.12,.325,.255,0),(.31,.235,.22,0),(.48,.275,.25,.01),(.70,.37,.29,.025),(1.05,.445,.345,.045),(1.38,.47,.375,.06),(1.62,.405,.36,.055)]
def sample(z):
    k=next((i for i in range(len(profile)-1) if profile[i+1][0]>=z),len(profile)-2)
    a,b=profile[k:k+2];t=(z-a[0])/(b[0]-a[0]);t=t*t*(3-2*t)
    return [a[j]+t*(b[j]-a[j]) for j in range(1,4)]
for j in range(M+1):
    t=j/M
    for i in range(N+1):
        a=-.30+(pi+.60)*i/N
        crown=1.33+.29*max(0,sin(a))**.65
        z=.025+(crown-.025)*t
        rx,ry,dy=sample(z)
        verts.append((rx*cos(a),ry*sin(a)+dy,z))
faces=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(M) for i in range(N)]
temp=mesh('Cinematic continuous tulip template',verts,faces,pink);finish(temp,True)
for ob in backs:
    ob.data=temp.data
    ob.modifiers.clear()
    solid=ob.modifiers.new('Upholstered continuous shell','SOLIDIFY');solid.thickness=.065;solid.offset=0
    bevel=ob.modifiers.new('Soft upholstery perimeter','BEVEL');bevel.width=.018;bevel.segments=3
    ob['source']='Northeastern ISEC Reflections011/022; photo-derived continuous petal/waist, product unverified'
bpy.data.objects.remove(temp,do_unlink=True)
remove_where(lambda o:o.name.startswith('Ground tall magenta tulip') and 'upholstered pedestal' in o.name)
seatmat=bpy.data.materials['Graphite task chair'].copy();seatmat.name='Tulip dark charcoal textile seat'
bs=next(n for n in seatmat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
bs.inputs['Base Color'].default_value=(.035,.028,.033,1);bs.inputs['Roughness'].default_value=.88;bs.inputs['Sheen Weight'].default_value=.22
for ob in bpy.data.objects:
    if ob.name.startswith('Ground tall magenta tulip') and 'seat cushion' in ob.name:
        ob.data.materials.clear();ob.data.materials.append(seatmat)
bpy.context.scene['cinematic_geometry_revision']='63 tulip continuous-shell trial'
print('Eight shared continuous tulip shells and source-visible dark seats; master save pending visual review')
