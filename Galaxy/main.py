import pygame
import sketch

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

screen = None
clock = None
done = False
stroke_color = BLACK
stroke_weight = 1

def size(size):
    global screen
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

def background(color):
    screen.fill(color)

def backgroundBlend(coef):
    color = (255 * coef, 255 * coef, 255 * coef)
    screen.fill(color, special_flags=pygame.BLEND_MULT)

def stroke(color):
    global stroke_color
    stroke_color = color;

def strokeWeight(weight):
    global stroke_weight
    stroke_weight = weight;

def point(start):
    rect = pygame.Rect(start[0], start[1], stroke_weight, stroke_weight)
    pygame.draw.rect(screen, stroke_color, rect)

def line(start, end):
    pygame.draw.line(screen, stroke_color, start, end, stroke_weight)    

def ellipse(center, axis):
    left = center[0] - axis[0] / 2
    top = center[1] - axis[1] / 2
    rect = pygame.Rect((left, top), axis)
    pygame.draw.ellipse(screen, stroke_color, rect, stroke_weight)

def get_size():
    return pygame.display.get_window_size()

if __name__ == "__main__":
    pygame.init()
    
    clock = pygame.time.Clock()
    
    sketch.setup()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        sketch.loop()
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()    
