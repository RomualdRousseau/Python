import numpy as np

from oscillators import *
from effects import *

ONE_PI = np.pi
TWO_PI = 2 * np.pi
HALF_PI = np.pi / 2

SAMPLING_RATE = 22050
BPM = 450
TICK = 60 / (16 * BPM)

WAVEFORMS = [
        triangle,
        ramp,
        sawtooth,
        square,
        noise,
        sin
        ]

EFFECTS = [
        (effect_frq_none, effect_env_none),             # None
        (effect_frq_slide, effect_env_none),            # Slide
        (effect_frq_vibrato, effect_env_none),          # Vibrato
        (effect_frq_drop, effect_env_none),             # Drop
        (effect_frq_none, effect_env_fade_in),          # Fade In
        (effect_frq_none, effect_env_fade_out),         # Fade Out
        (effect_frq_none, effect_env_none),             # Arpegio Fast
        (effect_frq_none, effect_env_none)              # Arpegio Slow
        ]

PITCHES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

last_note = 0
last_l = 0

def to_chromatic(p, o):
    return PITCHES.index(p) + 12 * o


def to_freq(n):
    return 65.41 * 2**(n / 12)


def set_speed(speed):
    pass


def generate_note(note, waveform, volume, effect, speed):
    global last_note
    global last_l
    l = speed * TICK
    if note == -1:
        y = np.zeros(int(l * SAMPLING_RATE))
        last_l = l
    else:
        t = np.linspace(0, 1, int(l * SAMPLING_RATE))
        x = l * t
        f = to_freq(note)
        s = WAVEFORMS[waveform]
        w = lambda t : EFFECTS[effect][0](t, to_freq(last_note), f)
        e = EFFECTS[effect][1]
        v = volume / 7
        if last_note == note:
            y = v * e(t) * s(TWO_PI * w(t) * (x + last_l))
            last_l += l
        else:
            y = v * e(t) * s(TWO_PI * w(t) * x)
            last_l = l 
    last_note = note
    return y


def to_sound_array(data, size = 16):
    t = np.uint8 if size == 8 else np.uint16
    r = (2**size - 1) / 2
    return (data * r).astype(t)


def stitch(x1):
    x2 = np.pad(x1, (1, 0), "constant")[:-1]
    i = np.argwhere(np.logical_and(x1 - x2 > 0, x1 * x2 < 0) == True)
    return x1[:i.max() - 1] if len(i) > 0 else x1


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    sample = np.concatenate((
        generate_note(to_chromatic("C", 4), 5, 7, 0, 12),
        generate_note(to_chromatic("C#", 4), 5, 7, 0, 12),
        generate_note(to_chromatic("C#", 4), 5, 7, 0, 12),
        generate_note(to_chromatic("C#", 4), 5, 7, 0, 12)
        ))
    plt.plot(sample)
    plt.show()
