import os
import csv
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BUTTONS = [
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_z,
    pygame.K_x,
]


class Pyco:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self._display = pygame.display.set_mode((512, 512))
        self._screen = pygame.Surface((128, 128))
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("monospace", 8, True)

        self._sprites = []
        with open("assets/spritesheet.csv") as csvfile:
            reader = csv.reader(csvfile)
            for r in reader:
                file, flags = r[0], int(r[1])
                img = pygame.image.load(os.path.join("assets", file)).convert_alpha()
                self._sprites.append((img, flags))

        with open("assets/map.csv") as csvfile:
            reader = csv.reader(csvfile)
            self._map = [[None if int(t) < 0 else int(t) for t in r] for r in reader]

        self._camera = (0, 0)

        self._init()

    def cls(self, color=BLACK):
        self._screen.fill(color)

    def fget(self, i, f):
        if i is None:
            return False
        else:
            return (self._sprites[i][1] & (1 << f)) > 0

    def spr(self, i, pos=(0, 0)):
        pos = (self._camera[0] + pos[0], self._camera[1] + pos[1])
        self._screen.blit(self._sprites[i][0], pos)

    def mget(self, pos):
        if pos[0] < 0 or pos[0] >= 128 or pos[1] < 0 or pos[1] >= 32:
            return None
        return self._map[pos[1]][pos[0]]

    def mset(self, pos, i):
        self._map[pos[1]][pos[0]] = i

    def map(self, pos=(0, 0)):
        pos = (self._camera[0] + pos[0], self._camera[1] + pos[1])
        cur = pos
        for i in range(32):
            for j in range(128):
                t = self._map[i][j]
                if t is not None:
                    self._screen.blit(self._sprites[t][0], cur)
                cur = (cur[0] + 8, cur[1])
            cur = (pos[0], cur[1] + 8)

    def btn(self, i):
        return pygame.key.get_pressed()[BUTTONS[i]]

    def camera(self, pos=(0, 0)):
        self._camera = pos

    def print(self, text, pos, col=WHITE):
        textsurface = self._font.render(text, True, col)
        self._screen.blit(textsurface, pos)

    def run(self):
        while not self._is_done(pygame.event.get()):
            self._update()
            self._draw()
            self._display.blit(
                pygame.transform.scale(self._screen, self._display.get_rect().size),
                (0, 0),
            )
            pygame.display.flip()
            self._clock.tick(30)
        pygame.quit()

    def _is_done(self, events):
        if not events:
            return False
        else:
            head, tail = events[0], events[1:]
            return head.type == pygame.QUIT or self._is_done(tail)
