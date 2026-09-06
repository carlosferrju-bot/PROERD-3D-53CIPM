import bpy

# Execute a cena completa no mesmo processo do Blender e renderize a animação.
exec(compile(open('blender/scripts/scene_full_realistic.py', 'r', encoding='utf-8').read(), 'scene_full_realistic.py', 'exec'))
main()

scene = bpy.context.scene
scene.render.filepath = '/tmp/proerd_full_frames/frame_'
# O Blender distribuído no runner Ubuntu foi compilado sem OpenImageDenoiser.
# Desabilitamos o denoise do Cycles para permitir o render por CPU.
if hasattr(scene.cycles, 'use_denoising'):
    scene.cycles.use_denoising = False
bpy.ops.wm.save_as_mainfile(filepath='/tmp/PROERD_Licao03_full_realistic.blend')
print('[PROERD 3D] Cena completa salva; iniciando render Cycles sem OIDN.')
bpy.ops.render.render(animation=True)
