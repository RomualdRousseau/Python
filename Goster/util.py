import math

NORMALS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

GRAVITY = 4

WALL = 0
ANIM = 1
COIN = 2
MONSTER = 3

PLAYER = 7
SKY = 4

TILE_ANIM = [0, 0, 0, 1, 0, 0, 0, -1]


def to_screen(pos):
    return (pos[0] * 8, pos[1] * 8)


def to_map(pos):
    return (int(pos[0] / 8), int(pos[1] / 8))
