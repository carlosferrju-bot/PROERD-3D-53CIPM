import bpy

# Execute a cena completa no mesmo processo do Blender e renderize a animação.
exec(compile(open('blender/scripts/scene_full_realistic.py', 'r', encoding='utf-8').read(), 'scene_full_realistic.py', 'exec'))
main()

scene = bpy.context.scene
scene.render.filepath = '/tmp/proerd_full_frames/frame_'
bpy.ops.wm.save_as_mainfile(filepath='/tmp/PROERD_Licao03_full_realistic.blend')
print('[PROERD 3D] Cena completa salva; iniciando render Cycles.')
bpy.ops.render.render(animation=True)
