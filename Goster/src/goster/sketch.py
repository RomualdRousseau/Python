from pyco import *
from util import *
from player import *
from monster import *


class Sketch(Pyco):
    def _init(self):
        global pyco
        pyco = self

        self.timer = 0
        self.score = 0

        self.player = Player(self)

        self.monsters = []
        for i in range(16, 32):
            for j in range(128):
                pos = (j, i)
                tile = pyco.mget(pos)
                if pyco.fget(tile, MONSTER):
                    monster = Monster(self, tile, to_screen(pos))
                    self.monsters.append(monster)
                    pyco.mset(pos, SKY)

    def _update(self):
        # Update map animation
        for i in range(16, 32):
            for j in range(128):
                pos = (j, i)
                tile = pyco.mget(pos)
                if pyco.fget(tile, ANIM):
                    pyco.mset(pos, tile + TILE_ANIM[pyco.timer])

        self.player.update()

        for monster in self.monsters:
            monster.update()

        self.timer = (self.timer + 1) % 8

    def _draw(self):
        player = self.player.get_position()
        pyco.camera((-player[0] + 8 * 8, -16 * 8))

        pyco.cls()

        pyco.map()

        for monster in self.monsters:
            monster.draw()

        self.player.draw()

        # HUD
        pyco.print("Score: %s" % (self.score), (0, 0))
