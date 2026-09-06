"""Primeira cena 3D de demonstração do PROERD 53ª CIPM.

Cena curta para validar o pipeline completo do GitHub Actions:
Blender -> cena 3D -> animação simples -> frames -> MP4.
"""

import bpy
import math
from mathutils import Vector

W, H, FPS = 1920, 1080, 30
DURATION = 6


def mat(name, color, metallic=0.0, roughness=0.5):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return m


def cube(name, loc, scale, material, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("Soft edges", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    o.data.materials.append(material)
    return o


def uv(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    return o


def text(name, body, loc, size, material, align="CENTER"):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0))
    o = bpy.context.object
    o.name = name
    o.data.body = body
    o.data.align_x = align
    o.data.align_y = "CENTER"
    o.data.size = size
    o.data.extrude = 0.012
    o.data.bevel_depth = 0.004
    o.data.materials.append(material)
    return o


def setup_camera():
    bpy.ops.object.camera_add(location=(0, -15, 7.2))
    cam = bpy.context.object
    cam.name = "CAMERA_SC01"
    cam.data.lens = 48
    bpy.context.scene.camera = cam
    target = Vector((0, 0, 2.6))
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return cam


def setup_lights():
    bpy.ops.object.light_add(type="AREA", location=(0, -3, 9))
    key = bpy.context.object
    key.data.energy = 1300
    key.data.shape = "DISK"
    key.data.size = 7

    bpy.ops.object.light_add(type="AREA", location=(-7, 1, 5))
    fill = bpy.context.object
    fill.data.energy = 700
    fill.data.size = 5
    fill.rotation_euler = (math.radians(55), 0, math.radians(-55))


def character(prefix, x, shirt_mat, hair_mat, skin_mat, z=0):
    # Personagens originais, em estilo 3D infantil, sem copiar os personagens do vídeo de referência.
    cube(prefix + "_body", (x, 0, 2.0 + z), (0.72, 0.45, 0.9), shirt_mat, 0.18)
    uv(prefix + "_head", (x, -0.02, 3.55 + z), (0.62, 0.58, 0.68), skin_mat)
    uv(prefix + "_hair", (x, -0.03, 4.05 + z), (0.64, 0.60, 0.28), hair_mat)
    jeans = mat(prefix + "_jeans", (0.08, 0.16, 0.28))
    cube(prefix + "_legL", (x - 0.28, 0, 0.75 + z), (0.20, 0.25, 0.65), jeans, 0.12)
    cube(prefix + "_legR", (x + 0.28, 0, 0.75 + z), (0.20, 0.25, 0.65), jeans, 0.12)
    eyes = mat(prefix + "_eyes", (0.02, 0.02, 0.02))
    uv(prefix + "_eyeL", (x - 0.21, -0.55, 3.62 + z), (0.07, 0.04, 0.09), eyes)
    uv(prefix + "_eyeR", (x + 0.21, -0.55, 3.62 + z), (0.07, 0.04, 0.09), eyes)


def main():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    navy = mat("PROERD Navy", (0.025, 0.09, 0.20), roughness=0.35)
    red = mat("PROERD Red", (0.75, 0.03, 0.05), roughness=0.35)
    white = mat("White", (0.96, 0.97, 0.98), roughness=0.6)
    blue = mat("Light Blue", (0.38, 0.70, 0.88), roughness=0.5)
    wood = mat("Wood", (0.30, 0.16, 0.08), roughness=0.65)
    skin = mat("Skin", (0.72, 0.45, 0.30), roughness=0.55)
    shirt1 = mat("Shirt Blue", (0.04, 0.28, 0.58), roughness=0.5)
    shirt2 = mat("Shirt Red", (0.75, 0.06, 0.08), roughness=0.5)
    hair1 = mat("Hair 1", (0.05, 0.025, 0.015), roughness=0.8)
    hair2 = mat("Hair 2", (0.16, 0.07, 0.025), roughness=0.8)

    # Ambiente
    cube("Floor", (0, 0, 0), (8, 7, 0.12), wood, 0.04)
    cube("BackWall", (0, 3.8, 4.2), (8, 0.12, 4.2), white, 0.02)
    cube("AccentWall", (-7.2, 1, 4.2), (0.12, 2.8, 4.2), blue, 0.02)
    cube("Rug", (0, 0.2, 0.15), (4.8, 2.8, 0.05), white, 0.08)

    # Sofá e TV
    cube("SofaBase", (0.2, 2.0, 1.15), (3.3, 0.75, 0.55), navy, 0.2)
    cube("SofaBack", (0.2, 2.55, 2.05), (3.3, 0.25, 1.1), navy, 0.2)
    cube("TV", (0, 3.25, 5.25), (3.1, 0.12, 1.65), navy, 0.12)
    cube("TVScreen", (0, 3.08, 5.25), (2.65, 0.04, 1.25), white, 0.03)

    # Identidade visual no ambiente
    text("Title", "LIÇÃO 03", (-4.9, 3.0, 6.4), 0.65, red)
    text("Subtitle", "RISCOS E CONSEQUÊNCIAS", (-4.0, 3.0, 5.7), 0.38, navy)
    text("Theme", "JOÃO FAZ AULA DE KARATÊ", (-3.4, 3.0, 5.15), 0.25, navy)

    character("JOAO", -1.45, shirt1, hair1, skin)
    character("MATHEUS", 1.45, shirt2, hair2, skin)

    # Placa PROERD estilizada
    cube("Badge", (5.7, 3.0, 4.8), (1.5, 0.08, 0.9), red, 0.12)
    text("BadgeText", "PROERD", (5.7, 2.88, 4.82), 0.42, white)
    text("UnitText", "53ª CIPM", (5.7, 2.88, 4.30), 0.20, white)

    cam = setup_camera()
    setup_lights()

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = W
    scene.render.resolution_y = H
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.frame_start = 1
    scene.frame_end = DURATION * FPS
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.filepath = "/tmp/proerd_frames/frame_"

    # Entrada dos personagens e leve aproximação da câmera.
    for prefix, start_x, end_x in (("JOAO", -5.0, -1.45), ("MATHEUS", 5.0, 1.45)):
        for suffix in ("_body", "_head", "_hair", "_legL", "_legR", "_eyeL", "_eyeR"):
            obj = bpy.data.objects.get(prefix + suffix)
            if obj:
                obj.location.x = start_x
                obj.keyframe_insert(data_path="location", frame=1)
                obj.location.x = end_x
                obj.keyframe_insert(data_path="location", frame=45)

    cam.location = (0, -16.5, 7.2)
    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (0, -15.0, 7.2)
    cam.keyframe_insert(data_path="location", frame=scene.frame_end)

    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath="/tmp/PROERD_SC01_demo.blend")
    print("[PROERD 3D] SC01 criada e salva em /tmp/PROERD_SC01_demo.blend")


if __name__ == "__main__":
    main()
