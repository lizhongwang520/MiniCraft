import pyglet


class Audio(object):
    def __init__(self, src):
        self.src = src
        self.player = None

    def play(self, recycle=False):
        # Create a player
        self.player = pyglet.media.Player()
        # Load a sound file
        sound = pyglet.media.load(self.src, streaming=False)
        # Resource enqueue
        self.player.queue(source=sound)
        # Events
        self.player.on_eos = pyglet.media.SourceGroup.loop
        # Play
        self.player.play()
