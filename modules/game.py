import pyglet
from pyglet import image
from pyglet.graphics import TextureGroup
from collections import deque


class Game(object):

    def __init__(self, scaler=None):
        self.scaler = scaler
        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(image.load(scaler.src).get_texture())
        self.world = {}
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.queue = deque()

    def __initialize(self):
        pass

    def add_block(self, position, texture, immediate=True):
        if position in self.world:
            print('remove block.....')

        self.world[position] = texture
        self.sectors.setdefault(self.scaler.sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)