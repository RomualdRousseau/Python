import math
import random
import numpy as np
from main import *

GRAVITATION_CONSTANT = 0.9

class Star:
    def __init__(self, center, majorAxis, theta):
        self.majorAxis = majorAxis
        self.minorAxis = majorAxis * random.gauss(0.5, 0.1)
        
        self.dw = random.gauss(0.75, 0.1)
        self.w = random.random() * math.pi * 2

        self.T = np.transpose([
            [math.cos(theta), -math.sin(theta), center[0]],
            [math.sin(theta),  math.cos(theta), center[1]],
        ])

    def update(self, dt):
        grav_force = random.gauss(0.1, 0.01) - random.gauss(0.1, 0.01) * GRAVITATION_CONSTANT
        self.dw += grav_force * dt
        self.w += self.dw * dt
        
        exp_force = random.gauss(0.1, 0.01)
        self.majorAxis += exp_force * dt
        self.minorAxis += exp_force * dt

    def draw(self):
        P = np.array([
            self.majorAxis * math.cos(self.w),
            self.minorAxis * math.sin(self.w),
            1
        ])

        C = np.array(get_size()) / 2
        
        point(P @ self.T + C)

