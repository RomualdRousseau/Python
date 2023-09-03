from util import *
from entity import Entity


class Monster(Entity):
    def __init__(self, pyco_, sprite, pos):
        super().__init__(layer=0, mask=1)

        global pyco
        pyco = pyco_

        self.sprite = sprite
        self.pos = (pos[0] + 4, pos[1] + 4)
        self.speed = -2

        self.update = self.update_walk
        self.draw = self.draw_walk

    def on_collide(self, caller, collision):
        if caller is None:
            if collision[0] != 0:
                self.speed *= -1
        elif collision[1] > 0:
            self.die()

    def get_position(self):
        return (self.pos[0] - 4, self.pos[1] - 4)

    def die(self):
        pyco.score += 10
        self.pos = (self.pos[0] - 4, self.pos[1] - 16)
        self.update = self.update_die
        self.draw = self.draw_die

    def update_walk(self):
        vel = (self.speed, GRAVITY)
        self.move(pyco, vel)

    def draw_walk(self):
        pyco.spr(self.sprite + int(pyco.timer / 4), self.get_position())

    def update_die(self):
        if self.pos[1] < 260:
            self.pos = (self.pos[0], self.pos[1] + 2)

    def draw_die(self):
        pyco.spr(self.sprite, self.get_position())
