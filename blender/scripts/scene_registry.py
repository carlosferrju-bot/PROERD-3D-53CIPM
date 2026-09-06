"""Registro central das cenas da Lição 03.

A duração e o conteúdo serão preenchidos após a decomposição do vídeo de referência.
"""

SCENES = [
    {
        "id": "SC01",
        "title": "Cena 01",
        "duration_seconds": None,
        "characters": [],
        "environment": None,
        "dialogue": [],
        "animation_notes": [],
    },
]


def get_scene(scene_id: str):
    return next((scene for scene in SCENES if scene["id"] == scene_id), None)
