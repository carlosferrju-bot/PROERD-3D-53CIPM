"""Bootstrap do projeto PROERD 3D.

Compatível com Blender 4.x e versões posteriores que usam o identificador
BLENDER_EEVEE_NEXT. O script escolhe automaticamente um engine EEVEE disponível.
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


def choose_eevee_engine():
    """Seleciona o identificador EEVEE aceito pela versão instalada."""
    available = {item.identifier for item in bpy.types.Scene.bl_rna.properties["render"].fixed_type.properties["engine"].enum_items}
    # Blender 4.0 usa BLENDER_EEVEE; versões posteriores podem usar NEXT.
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if engine in available:
            return engine
    raise RuntimeError(f"Nenhum engine EEVEE disponível. Engines: {sorted(available)}")


def configure_render():
    scene = bpy.context.scene
    engine = choose_eevee_engine()
    scene.render.engine = engine
    scene.render.resolution_x = WIDTH
    scene.render.resolution_y = HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    print(f"[PROERD 3D] Render engine selecionado: {engine}")


def main():
    for name in COLLECTIONS:
        ensure_collection(name)

    configure_render()
    print("[PROERD 3D] Projeto inicializado: 1920x1080 @ 30 FPS")


if __name__ == "__main__":
    main()
