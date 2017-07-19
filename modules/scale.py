class Scale(object):

    def __init__(self, src=None, textures=None):
        self.src = src
        self.features = {}

        for key, value in textures.items():
            self.features[key] = self.__tex_coords(value)

    '''
        Each face has four vertices(x, y, z), totally six faces, size 2*n;
    '''
    def cube_vertices(self, x, y, z, n):
        return [
            x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n,  # top
            x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,  # bottom
            x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,  # left
            x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,  # right
            x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,  # front
            x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n,  # back
        ]

    '''
        According to percentage 1x1, divided into 4x4(n), transfer to percentage based coord.


        (0, 0) -> (3, 3)
        ------|------|------|------
              |      |      |(3, 3)
        ------|------|------|------
              |      |      |
        ------|------|------|------
              |      |      |
        ------|------|------|------
        (0, 0)|      |      |
        ------|------|------|------      
        
        [(top_texture), (bottom_texture), (side_texture)]

    '''
    def __tex_coord(self, x, y, n=4):
        m = 1.0 / n
        dx = x * m
        dy = y * m
        return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

    '''
        Textrues coords, sequences: (top, bottom, side, side, side, side)
    '''
    def __tex_coords(self, arg):
        [top, bottom, side] = arg
        top = self.__tex_coord(*top)
        bottom = self.__tex_coord(*bottom)
        side = self.__tex_coord(*side)
        result = []
        result.extend(top)
        result.extend(bottom)
        # Each side face is all the same
        result.extend(side * 4)
        return result

    def normalize(self, position):
        x, y, z = position
        x, y, z = (int(round(x)), int(round(y)), int(round(z)))
        return (x, y, z)

    def sectorize(self, position):
        x, y, z = self.normalize(position)
        # Integer division
        x, y, z = x // 16, y // 16, z // 16
        return (x, 0, z)
