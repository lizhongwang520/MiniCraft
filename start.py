#!/usr/bin/env python3

import pyglet

from modules.audio import Audio
from modules.scale import Scale
from modules.window import Window
from modules.game import Game


# Set textures src
src = 'textures/texture.png'

# Set textures coord
textures = {'GRASS': [(1, 0), (0, 1), (0, 0)], 'SAND': [(1, 1), (1, 1), (1, 1)], 'BRICK': [(2, 0), (2, 0), (2, 0)], 'STONE': [(2, 1), (2, 1), (2, 1)]}

# Window
Window(fullscreen=True, caption='MiniCraft', model=Game(Scale(src, textures)))

# Music
Audio('audios/background.wav').play(recycle=True)

# Run the game
pyglet.app.run()
