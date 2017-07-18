#!/usr/bin/env python3

import pyglet

from pyglet.gl import *
from modules.audio import Audio
from modules.scale import Scale
from modules.window import Window
from modules.game import Game

# Set textures src
src = 'textures/texture.png'

# Set textures coord
textures = {'GRASS': [(1, 0), (0, 1), (0, 0)], 'SAND': [(1, 1), (1, 1), (1, 1)], 'BRICK': [(2, 0), (2, 0), (2, 0)], 'STONE': [(2, 1), (2, 1), (2, 1)]}

# Music
Audio('audios/background.wav').play(recycle=True)

# Window
Window(fullscreen=False, caption='MiniCraft', model=Game(Scale(src, textures)))


# Global settings
glClearColor(0.5, 0.69, 1.0, 1)
glEnable(GL_CULL_FACE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
# Setup fog
glEnable(GL_FOG)
glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
glHint(GL_FOG_HINT, GL_DONT_CARE)
glFogi(GL_FOG_MODE, GL_LINEAR)
glFogf(GL_FOG_START, 20.0)
glFogf(GL_FOG_END, 60.0)

# Run the game
pyglet.app.run()
