import star
import math
from main import *

number_of_stars = 2000
distance_stars = 0.1
min_axis_len = 1

stars = []

def setup():
    size((800, 800))
    stroke((255, 128, 192));
    strokeWeight(2);
    
    center = (0, 0)
    
    dtheta = 2 * (math.pi / number_of_stars)
    
    for i in range(0, number_of_stars):
        new_star = star.Star(center, i * distance_stars + min_axis_len, i * dtheta)
        stars.append(new_star)
    
def loop():
    backgroundBlend(0.5)
    
    for star in stars:
        star.update(1 / 60)
    
    for star in stars:
        star.draw()

