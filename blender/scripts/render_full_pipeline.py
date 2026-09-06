import bpy

# Executa a cena completa no mesmo processo do Blender.
exec(compile(open('blender/scripts/scene_full_realistic.py', 'r', encoding='utf-8').read(), 'scene_full_realistic.py', 'exec'))
main()

scene = bpy.context.scene
scene.render.filepath = '/tmp/proerd_full_frames/frame_'

# Renderização final otimizada: EEVEE mantém os materiais, iluminação, câmera
# e animação da cena, mas evita o custo extremo do Cycles CPU no runner.
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

bpy.ops.wm.save_as_mainfile(filepath='/tmp/PROERD_Licao03_full_realistic.blend')
print('[PROERD 3D] Cena completa salva; iniciando render final otimizado em EEVEE.')
bpy.ops.render.render(animation=True)
