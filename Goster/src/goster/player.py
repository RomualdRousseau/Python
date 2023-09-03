from pyco import WHITE
from util import *
from entity import Entity


class Player(Entity):
    def __init__(self, pyco_):
        super().__init__(layer=1, mask=0)

        global pyco
        pyco = pyco_

        self.respawn()

    def get_position(self):
        return (self.pos[0] - 4, self.pos[1] - 4)

    def on_collide(self, caller, collision):
        if caller is None:
            if collision[1] > 0:
                self.jump = self.jump_power
            elif collision[1] < 0:
                self.jump = 0
        elif collision[1] <= 0:
            self.die()

    def respawn(self):
        self.layer = 1
        self.dead = False
        self.pos = (8.5 * 8, 29.5 * 8)
        self.speed = 4
        self.jump = 0
        self.jump_power = 8

        self.update = self.update_walk
        self.draw = self.draw_walk

    def die(self):
        self.layer = 0
        self.dead = True
        self.pos = (self.pos[0] - 4, self.pos[1] - 16)
        self.update = self.update_die
        self.draw = self.draw_die

    def update_walk(self):
        vel = (0, GRAVITY)

        if pyco.btn(0):
            vel = (vel[0] - self.speed, vel[1])
        if pyco.btn(1):
            vel = (vel[0] + self.speed, vel[1])
        if pyco.btn(4) and self.jump < self.jump_power:
            vel = (vel[0], vel[1] - GRAVITY * 2)
            self.jump += 1

        self.move(pyco, vel)

        pos = to_map(self.pos)
        tile = pyco.mget(pos)
        if pyco.fget(tile, COIN):
            pyco.score += 1
            pyco.mset(pos, SKY)

        if self.pos[1] > 248:
            self.die()

    def draw_walk(self):
        pyco.spr(PLAYER + int(pyco.timer / 4), self.get_position())

    def update_die(self):
        if self.pos[1] < 260:
            self.pos = (self.pos[0], self.pos[1] + 2)
        elif pyco.btn(5):
            self.respawn()

    def draw_die(self):
        pyco.spr(11, self.get_position())
