import os
import bpy

# Executa a cena completa no mesmo processo do Blender.
exec(compile(open('blender/scripts/scene_full_realistic.py', 'r', encoding='utf-8').read(), 'scene_full_realistic.py', 'exec'))
main()

scene = bpy.context.scene
scene.render.filepath = '/tmp/proerd_full_frames/frame_'

# Blender 4.2 instalado no runner usa BLENDER_EEVEE.
# EEVEE mantém os materiais, iluminação, câmera e animação da cena,
# evitando o custo extremo do Cycles CPU no runner.
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# O GitHub-hosted runner encerra cada job após 6 horas. Para que a
# renderização não seja perdida no fim desse limite, o workflow divide
# os 2111 frames em blocos independentes e informa o intervalo por
# variáveis de ambiente.
frame_start = int(os.environ.get('FRAME_START', scene.frame_start))
frame_end = int(os.environ.get('FRAME_END', scene.frame_end))
scene.frame_start = frame_start
scene.frame_end = frame_end
scene.frame_set(frame_start)

bpy.ops.wm.save_as_mainfile(filepath='/tmp/PROERD_Licao03_full_realistic.blend')
print(f'[PROERD 3D] Cena salva; renderizando frames {frame_start} até {frame_end} em EEVEE.')
bpy.ops.render.render(animation=True)
