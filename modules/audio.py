import pyglet


class Audio(object):
    def __init__(self, src):
        self.src = src
        self.player = None

    def play(self, recycle=False):
        # Load a resource
        sound = pyglet.media.load(self.src, streaming=False)

        # Control music playing with SourceGroup
        source_group = pyglet.media.SourceGroup(sound.audio_format, None)
        source_group.loop = bool(recycle)
        source_group.queue(sound)

        # Init a player
        self.player = pyglet.media.Player()

        # Resource enqueue
        self.player.queue(source_group)

        # Play
        self.player.play()
