import sys
import pygame as pg
from pygame.locals import *

from synth import *
from song import *

BUFFERS_COUNT = 3

channel = None
generate_func = None
buffers = [ None for i in range(BUFFERS_COUNT) ]
buf_cur = 0
song_cur = 0
patt_cur = 0

def generate_all_sounds(song):
    data = []
    for i in range(0, 100):
        data = np.concatenate((data, generate_note(*song[i])))
    return pg.mixer.Sound(to_sound_array(data, -pg.mixer.get_init()[1]))


def generate_sound(i, song):
    #data = generate_note(*song[0])
    data = generate_note(*song[i])
    return pg.mixer.Sound(to_sound_array(data, -pg.mixer.get_init()[1]))


def queue_sound():
    global song_cur
    global buf_cur

    if song_cur <= len(SONG): 
        channel.queue(buffers[buf_cur])
        buf_cur = (buf_cur + 1) % BUFFERS_COUNT

    song_cur += 1
    if song_cur < len(SONG):
        buffers[buf_cur] = generate_func(song_cur)
    
    return True


def start_sound(sound):
    global generate_func
    global channel
    
    generate_func = lambda i: generate_sound(i, sound)
    
    channel = pg.mixer.find_channel()
    channel.set_endevent(USEREVENT + 1)

    buffers[0] = generate_func(0)
    queue_sound()

def setup():
    global patt_cur
    start_sound(SONG)
    print(patt_cur, SONG[patt_cur])
    patt_cur += 1


def loop():
    global patt_cur
    events = pg.event.get()
    for event in events:
        if event.type == channel.get_endevent():
            queue_sound()
            if patt_cur < len(SONG):
                print(patt_cur, SONG[patt_cur])
                patt_cur += 1
    return patt_cur < len(SONG)


def main():
    pg.mixer.pre_init(frequency = SAMPLING_RATE, size = -8, channels = 1, buffer = 256)
    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock() 

    setup()
    while(loop()):
        clock.tick(60)

    pg.mixer.quit()


if __name__ == "__main__":
    sys.exit(main())
