import pyglet


class Audio(object):
    def __init__(self, src):
        self.src = src
        self.player = None
        self.settings = {
            'recycle': False
        }

    def on_eos(self):
        if self.settings['recycle']:
            self.player.play()

    def play(self, recycle=False):
        self.settings['recycle'] = recycle

        music = pyglet.media.load(self.src, streaming=False)
        self.player = music.play()

        # Events
        self.player.on_eos = self.on_eos

