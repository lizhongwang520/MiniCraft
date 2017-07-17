import pyglet


class Window(pyglet.window.Window):
    def __init__(self, *args, model, **kw):
        super(Window, self).__init__(*args, **kw)

        # Hide cursor
        self.exclusive = False

        # Current positon
        self.position = (0, 0, 0)

        # Main event loop
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)

    def on_resize(self, width, height):
        pass

    def on_draw(self):
        pass

    def update(self, dt):
        pass


