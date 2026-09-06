import bpy, math
from mathutils import Vector

W,H,FPS=1280,720,24
DURATION=87.95

def mat(name, base, rough=.5, metallic=0.0, subsurface=0.0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*base,1)
    bs.inputs['Roughness'].default_value=rough
    bs.inputs['Metallic'].default_value=metallic
    if 'Subsurface Weight' in bs.inputs: bs.inputs['Subsurface Weight'].default_value=subsurface
    elif 'Subsurface' in bs.inputs: bs.inputs['Subsurface'].default_value=subsurface
    return m

def smooth(obj):
    if hasattr(obj.data,'polygons'):
        for p in obj.data.polygons: p.use_smooth=True

def uv(name,loc,scale,material,seg=48,rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    smooth(o);o.data.materials.append(material)
    return o

def cube(name,loc,scale,material,bevel=.08):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        b=o.modifiers.new('Rounded edges','BEVEL');b.width=bevel;b.segments=4
    o.data.materials.append(material);return o

def cyl(name,loc,radius,depth,material,rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth,location=loc,rotation=rot or (0,0,0))
    o=bpy.context.object;o.name=name;smooth(o);o.data.materials.append(material);return o

def text(name,body,loc,size,material,rot=(math.pi/2,0,0)):
    bpy.ops.object.text_add(location=loc,rotation=rot)
    o=bpy.context.object;o.name=name;o.data.body=body;o.data.align_x='CENTER';o.data.size=size;o.data.extrude=.008;o.data.bevel_depth=.002;o.data.materials.append(material);return o

def curve_line(name,pts,bevel,material):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=bevel;cu.bevel_resolution=4
    sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for bp,p in zip(sp.bezier_points,pts): bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(material);return ob

SKIN=mat('Skin',(0.62,0.34,0.20),.42,subsurface=.18)
SKIN2=mat('SkinLight',(0.78,0.52,0.34),.42,subsurface=.18)
HAIR=mat('Hair',(0.025,0.012,0.008),.82)
HAIR2=mat('HairBrown',(0.16,0.055,0.018),.72)
WHITE=mat('EyeWhite',(.98,.98,.98),.18)
IRIS=mat('Iris',(.06,.16,.22),.18)
BLACK=mat('Black',(.008,.006,.005),.25)
GREEN=mat('JoaoShirt',(.04,.27,.10),.48)
BLUE=mat('MateusShirt',(.10,.12,.42),.48)
JEANS=mat('Jeans',(.035,.07,.15),.58)
SHOE=mat('Shoes',(.018,.018,.02),.32)
RED=mat('PROERDRed',(.72,.035,.045),.32)
NAVY=mat('Navy',(.025,.08,.16),.4)
WOOD=mat('Wood',(.23,.11,.045),.62)
WALL=mat('Wall',(.88,.90,.92),.72)
RUG=mat('Rug',(.82,.84,.86),.9)

def make_human(name,x,shirt,hair,skin):
    p={}
    p['torso']=cube(name+'_torso',(x,0,2.15),(.47,.27,.72),shirt,.15)
    p['neck']=cyl(name+'_neck',(x,-.01,2.92),.16,.22,skin)
    p['head']=uv(name+'_head',(x,-.02,3.58),(.49,.43,.58),skin)
    p['earL']=uv(name+'_earL',(x-.49,-.01,3.57),(.09,.07,.14),skin)
    p['earR']=uv(name+'_earR',(x+.49,-.01,3.57),(.09,.07,.14),skin)
    p['hair']=uv(name+'_hair',(x,-.03,4.03),(.53,.46,.28),hair)
    for i,dx in enumerate([-.34,-.17,0,.17,.34]): p[f'fringe{i}']=uv(name+f'_fringe{i}',(x+dx,-.43,3.91),(.13,.10,.18),hair)
    for side,sx in [('L',x-.19),('R',x+.19)]:
        p['eye'+side]=uv(name+'_eye'+side,(sx,-.405,3.64),(.095,.055,.075),WHITE)
        p['iris'+side]=uv(name+'_iris'+side,(sx,-.457,3.64),(.035,.018,.04),IRIS)
        p['brow'+side]=curve_line(name+'_brow'+side,[(sx-.09,-.455,3.82),(sx,-.47,3.85),(sx+.09,-.455,3.82)],.018,BLACK)
    p['nose']=uv(name+'_nose',(x,-.47,3.48),(.055,.05,.11),skin)
    p['mouth']=curve_line(name+'_mouth',[(x-.13,-.46,3.31),(x,-.49,3.27),(x+.13,-.46,3.31)],.018,BLACK)
    for side,sx in [('L',x-.62),('R',x+.62)]:
        p['arm'+side]=cyl(name+'_arm'+side,(sx,0,2.18),.14,.95,shirt,rot=(0,math.radians(90),0))
        p['hand'+side]=uv(name+'_hand'+side,(sx + (-.07 if side=='L' else .07),-.01,1.69),(.15,.13,.16),skin)
    for side,sx in [('L',x-.23),('R',x+.23)]:
        p['leg'+side]=cyl(name+'_leg'+side,(sx,.02,.91),.18,1.55,JEANS)
        p['shoe'+side]=cube(name+'_shoe'+side,(sx,-.12,.17),(.25,.40,.12),SHOE,.07)
    return p

def setup_room():
    cube('Floor',(0,0,-.12),(10,8,.12),WOOD,.03)
    cube('BackWall',(0,4.3,4),(10,.10,4),WALL,.02)
    cube('SideWall',(-7.5,0,4),(0.1,4.3,4),WALL,.02)
    cube('Rug',(0,.7,.02),(5.5,3.4,.04),RUG,.05)
    cube('SofaBase',(1.0,2.8,.95),(3.3,.85,.55),NAVY,.22)
    cube('SofaBack',(1.0,3.45,1.9),(3.3,.25,1.1),NAVY,.22)
    for x in [-1.0,1.0,3.0]: cube('Cushion'+str(x),(x,2.95,1.65),(.85,.18,.55),NAVY,.15)
    cube('Table',(0,-.9,.75),(2.0,1.0,.12),WOOD,.08)
    for x in [-1.6,1.6]:
        for y in [-.55,.55]: cyl('TableLeg',(x,y,.37),.08,.75,WOOD)
    cube('TVFrame',(0,3.9,5.0),(3.0,.12,1.65),BLACK,.08)
    cube('TVScreen',(0,3.75,5.0),(2.72,.04,1.37),BLACK,.02)
    cube('PROERDPlate',(5.8,3.85,4.8),(1.2,.07,.62),RED,.08)
    text('PROERDPlateText','PROERD',(5.8,3.73,4.8),.42,WHITE)
    cube('PhotoFrame',(-5.7,3.8,5.0),(1.2,.06,.85),WOOD,.05)
    cube('Photo',(-5.7,3.72,5.0),(1.05,.02,.70),mat('Sea',(.12,.52,.68),.55),.01)

def lights():
    bpy.ops.object.light_add(type='AREA',location=(-3,-3,7));key=bpy.context.object;key.data.energy=900;key.data.size=5
    key.rotation_euler=(math.radians(20),0,math.radians(-25))
    bpy.ops.object.light_add(type='AREA',location=(5,2,5));fill=bpy.context.object;fill.data.energy=600;fill.data.size=4
    fill.rotation_euler=(math.radians(65),0,math.radians(120))
    bpy.ops.object.light_add(type='AREA',location=(0,4,7));rim=bpy.context.object;rim.data.energy=700;rim.data.size=3
    rim.rotation_euler=(0,0,math.pi)

def camera_setup():
    bpy.ops.object.camera_add(location=(0,-15,5.0));cam=bpy.context.object;cam.data.lens=52;bpy.context.scene.camera=cam
    target=Vector((0,1.3,2.5));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();return cam

def animate_talk(parts,start,end,gesture=False):
    for f in range(start,end+1,12):
        if 'mouth' in parts:
            s=1.0 if ((f-start)//12)%2==0 else .55
            parts['mouth'].scale=(1,s,1);parts['mouth'].keyframe_insert('scale',frame=f)
        if gesture and 'armR' in parts:
            a=.12 if ((f-start)//12)%2==0 else -.18
            parts['armR'].rotation_euler=(0,math.radians(90),a);parts['armR'].keyframe_insert('rotation_euler',frame=f)

def make_thought_bubble():
    bubblemat=mat('Bubble',(.98,.99,1),.25)
    for i in range(9):
        ang=math.radians(180+i*22);x=-1.0+3.0*math.cos(ang);z=4.0+1.1*math.sin(ang)
        uv('Bubble'+str(i),(x,0.0,z),(.55,.08,.45),bubblemat)
    cube('MiniRoom',(-1.0,.12,3.95),(2.0,.05,1.0),WALL,.02)
    mini1=make_human('AUGUSTO',-1.8,BLUE,HAIR2,SKIN2)
    mini2=make_human('MATEUS_THOUGHT',-.2,GREEN,HAIR,SKIN2)
    for p in mini1.values(): p.scale*=.48
    for p in mini2.values(): p.scale*=.48

def make_karate_area():
    cube('DojoFloor',(0,0,0),(6,5,.10),mat('Tatami',(.55,.43,.20),.8),.02)
    cube('DojoWall',(0,4.5,3.0),(6,.10,3),WALL,.02)
    text('KarateSign','KARATÊ',(0,4.35,5.1),.6,RED)

def configure_render(scene):
    scene.render.engine='CYCLES'
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    if hasattr(scene.cycles,'preview_samples'): scene.cycles.preview_samples=8
    scene.render.resolution_x=W;scene.render.resolution_y=H;scene.render.resolution_percentage=100
    scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=round(DURATION*FPS)
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    scene.render.filepath='/tmp/proerd_full_frames/frame_'
    try: scene.view_settings.look='AgX - Medium High Contrast'
    except: pass

def main():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    setup_room();lights();cam=camera_setup()
    joao=make_human('JOAO',-1.8,GREEN,HAIR,SKIN2)
    mateus=make_human('MATEUS',1.7,BLUE,HAIR2,SKIN2)
    for p in mateus.values(): p.scale=(.001,.001,.001);p.keyframe_insert('scale',frame=1);p.scale=(1,1,1);p.keyframe_insert('scale',frame=1190)
    make_thought_bubble()
    title=text('Title','LIÇÃO 03  •  RISCOS E CONSEQUÊNCIAS',(0,3.65,6.45),.48,RED)
    sub=text('Sub','JOÃO FAZ AULA DE KARATÊ',(0,3.64,5.9),.32,NAVY)
    title.keyframe_insert('scale',frame=1);title.keyframe_insert('scale',frame=85);title.scale=(.001,.001,.001);title.keyframe_insert('scale',frame=130)
    sub.keyframe_insert('scale',frame=1);sub.keyframe_insert('scale',frame=85);sub.scale=(.001,.001,.001);sub.keyframe_insert('scale',frame=130)
    cam.location=(0,-16,5.2);cam.keyframe_insert('location',frame=1)
    cam.location=(-1.5,-14,4.8);cam.keyframe_insert('location',frame=160)
    cam.location=(0,-15,5.0);cam.keyframe_insert('location',frame=650)
    cam.location=(1.0,-13.7,4.9);cam.keyframe_insert('location',frame=1180)
    cam.location=(0,-16,5.2);cam.keyframe_insert('location',frame=1500)
    cam.location=(0,-15,5.0);cam.keyframe_insert('location',frame=2111)
    animate_talk(joao,190,1185,gesture=True)
    joao['head'].rotation_euler=(0,0,math.radians(-5));joao['head'].keyframe_insert('rotation_euler',frame=520)
    joao['head'].rotation_euler=(0,0,math.radians(5));joao['head'].keyframe_insert('rotation_euler',frame=720)
    joao['head'].rotation_euler=(0,0,0);joao['head'].keyframe_insert('rotation_euler',frame=900)
    thought=[o for o in bpy.data.objects if o.name.startswith('Bubble') or o.name.startswith('MiniRoom') or o.name.startswith('AUGUSTO') or o.name.startswith('MATEUS_THOUGHT')]
    for o in thought:
        o.scale=(.001,.001,.001);o.keyframe_insert('scale',frame=1);o.scale=(1,1,1);o.keyframe_insert('scale',frame=430);o.keyframe_insert('scale',frame=1050);o.scale=(.001,.001,.001);o.keyframe_insert('scale',frame=1150)
    animate_talk(mateus,1200,1540,gesture=True)
    animate_talk(joao,1540,1900,gesture=True)
    dojo_start=1920
    for nm in ['SofaBase','SofaBack','TVFrame','TVScreen','Table','PhotoFrame','Photo','PROERDPlate','PROERDPlateText']:
        o=bpy.data.objects.get(nm)
        if o:
            o.keyframe_insert('scale',frame=dojo_start-1);o.scale=(.001,.001,.001);o.keyframe_insert('scale',frame=dojo_start+20)
    make_karate_area()
    gi=make_human('JOAO_KARATE',0,WHITE,HAIR,SKIN2)
    belt=cube('BlackBelt',(0,-.01,2.12),(.52,.30,.08),BLACK,.03)
    for p in gi.values(): p.scale*=1.05
    gi['armL'].rotation_euler=(0,math.radians(90),math.radians(25));gi['armL'].keyframe_insert('rotation_euler',frame=dojo_start+20);gi['armL'].rotation_euler=(0,math.radians(90),math.radians(-35));gi['armL'].keyframe_insert('rotation_euler',frame=dojo_start+70)
    gi['armR'].rotation_euler=(0,math.radians(90),math.radians(-25));gi['armR'].keyframe_insert('rotation_euler',frame=dojo_start+20);gi['armR'].rotation_euler=(0,math.radians(90),math.radians(35));gi['armR'].keyframe_insert('rotation_euler',frame=dojo_start+70)
    scene=bpy.context.scene;configure_render(scene);scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath='/tmp/PROERD_Licao03_full_realistic.blend')
    print('[PROERD] Full 87.95s Cycles scene created.')

if __name__=='__main__': main()
