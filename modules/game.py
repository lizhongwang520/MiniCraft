import pyglet
import time
import random

from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from collections import deque


class Game(object):

    def __init__(self, scaler=None):
        self.settings = {
            'SECTOR_SIZE': 16,
            'WALKING_SPEED': 5,
            'FLYING_SPEED': 15,
            'GRAVITY': 20.0,
            'MAX_JUMP_HEIGHT': 1.0,
            'TERMINAL_VELOCITY': 50,
            'PLAYER_HEIGHT': 2,
            'FACES': {
                (0, 1, 0),
                (0, -1, 0),
                (-1, 0, 0),
                (1, 0, 0),
                (0, 0, 1),
                (0, 0, -1)
            }
        }
        self.scaler = scaler
        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(image.load(scaler.src).get_texture())
        self.world = {}
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.queue = deque()

        self.__initialize()

    def __initialize(self):
        n = 80
        s = 1
        y = 0
        for x in range(-n, n + 1, s):
            for z in range(-n, n + 1, s):
                self.add_block((x, y - 2, z), self.scaler.features['GRASS'], immediate=False)
                self.add_block((x, y - 3, z), self.scaler.features['STONE'], immediate=False)
                if x in (-n, n) or z in (-n, n):
                    for dy in range(-2, 3):
                        print(self.scaler.features['STONE'])
                        self.add_block((x, y + dy, z), self.scaler.features['STONE'], immediate=False)

        o = n - 10
        for _ in range(120):
            a = random.randint(-o, o)  # x position of the hill
            b = random.randint(-o, o)  # z position of the hill
            c = -1  # base of the hill
            h = random.randint(1, 6)  # height of the hill
            s = random.randint(4, 8)  # 2 * s is the side length of the hill
            d = 1  # how quickly to taper off the hills
            t = random.choice([self.scaler.features['GRASS'], self.scaler.features['SAND'], self.scaler.features['BRICK']])
            for y in range(c, c + h):
                for x in range(a - s, a + s + 1):
                    for z in range(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                s -= d  # decrement side lenth so hills taper off


    def add_block(self, position, texture, immediate=True):
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(self.scaler.sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def show_block(self, position, immediate=True):
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        x, y, z = position
        vertex_data = self.scaler.cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group, ('v3f/static', vertex_data), ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def remove_block(self, position, immediate=True):
        del self.world[position]
        self.sectors[self.scaler.sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def _hide_block(self, position):
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = self.scaler.normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in self.settings['FACES']:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def check_neighbors(self, position):
        x, y, z = position
        for dx, dy, dz in self.settings['FACES']:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def _enqueue(self, func, *arg):
        self.queue.append((func, arg))

    def _dequeue(self):
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        start = time.clock()
        while self.queue and time.clock() - start < 1.0 / 60:
            self._dequeue()

    def process_entire_queue(self):
        while self.queue:
            self._dequeue()