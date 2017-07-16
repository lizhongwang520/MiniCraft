import pyglet


class Window(pyglet.window.Window):
    def __init__(self, *args, **kw):
        super(Window, self).__init__(*args, **kw)

    def on_resize(self, width, height):
        pass

    def on_draw(self):
        pass

