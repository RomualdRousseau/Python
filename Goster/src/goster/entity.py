from util import *

ENTITIES = []


class Entity:
    def __init__(self, pos=(0, 0), layer=0, mask=0):
        self.pos = pos
        self.layer = layer
        self.mask = mask
        ENTITIES.append(self)

    def on_collide(self, caller, collision):
        pass

    def move(self, pyco, vel):
        col, hit = self.collide_map(pyco, self.pos, vel)
        if hit:
            self.on_collide(None, col)

        self.pos = (self.pos[0] + vel[0] + col[0], self.pos[1] + vel[1] + col[1])
        self.pos = self.limit_borders(self.pos)

        for e in ENTITIES:
            if e != self and (e.layer & self.mask) > 0:
                col, hit = self.collide_sprite(self.pos, e.pos)
                if hit:
                    self.on_collide(e, col)
                    e.on_collide(self, col)

    def collide_sprite(self, source, target):
        v = (source[0] - target[0], source[1] - target[1])
        d = math.sqrt(v[0] ** 2 + v[1] ** 2)
        if d < 8:
            return v, True
        else:
            return v, False

    def collide_map(self, pyco, pos, vel):
        def collide_tile(pyco, pos, vel, vec, acc):
            target_pos = (
                pos[0] + vel[0] * abs(vec[0]) + 4 * vec[0],
                pos[1] + vel[1] * abs(vec[1]) + 4 * vec[1],
            )
            tile_pos = to_map(target_pos)
            tile = pyco.mget(tile_pos)
            if pyco.fget(tile, WALL):
                tile_pos = to_screen(tile_pos)
                col = (tile_pos[0] - target_pos[0], tile_pos[1] - target_pos[1])
                return (acc[0] + col[0] * vec[0], acc[1] + col[1] * vec[1]), True
            else:
                return acc, False

        n_hit = 0
        col = (0, 0)
        for vec in NORMALS:
            col, hit = collide_tile(pyco, pos, vel, vec, col)
            n_hit += 1 if hit else 0

        if n_hit == 4 and col == (0, 0):
            col = (0, -8)

        return col, n_hit > 0

    def limit_borders(self, pos):
        (x, y) = pos
        if x < 8.5 * 8:
            x = 8.5 * 8
        elif x > 120.5 * 8:
            x = 120.5 * 8
        if y < 0:
            y = 0
        elif y > 31.5 * 8:
            y = 31.5 * 8
        return (x, y)
