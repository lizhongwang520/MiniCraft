#!/usr/bin/env python3

import pyglet
import modules.audio as _audio_manager
import modules.window as _window_manager

window = _window_manager.Window(fullscreen=True, caption='MiniCraft')
window.set_exclusive_mouse(True)

# Music
_audio_manager.Audio('audios/background.wav').play(recycle=True)

# Run the game
pyglet.app.run()
