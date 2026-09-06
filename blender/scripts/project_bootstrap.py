"""Bootstrap do projeto PROERD 3D.

Execute no Blender via:
    blender --background --python blender/scripts/project_bootstrap.py

O script cria a estrutura básica de coleções, configura o render em Full HD
16:9 e deixa a cena pronta para receber os assets e animações.
"""

import bpy

WIDTH = 1920
HEIGHT = 1080
FPS = 30

COLLECTIONS = [
    "PROERD_SCENE",
    "CHARACTERS",
    "ENVIRONMENTS",
    "PROPS",
    "CAMERAS",
    "LIGHTS",
    "AUDIO",
]


def ensure_collection(name: str):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def configure_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = WIDTH
    scene.render.resolution_y = HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False


def main():
    for name in COLLECTIONS:
        ensure_collection(name)

    configure_render()
    print("[PROERD 3D] Projeto inicializado: 1920x1080 @ 30 FPS")


if __name__ == "__main__":
    main()
