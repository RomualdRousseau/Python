import numpy as np

ONE_PI = np.pi
TWO_PI = 2 * np.pi
HALF_PI = np.pi / 2


def effect_frq_none(t, f0, f1):
    return f1

def effect_frq_slide(t, f0, f1):
    return (f1 - f0) * t + f0

def effect_frq_vibrato(t, f0, f1):
    return f1 + 1.06 * np.sin(TWO_PI * 6 * t)

def effect_frq_drop(t, f0, f1):
    return f1 * (1 - 0.06 * np.exp(-TWO_PI * (1 - t)))

def effect_env_none(t):
    return (1 - np.exp(-TWO_PI * t * 8)) * (1 - np.exp(-TWO_PI * (1 - t) * 8))

def effect_env_fade_in(t):
    return effect_env_none(t) * np.exp(-TWO_PI * (1 - t))

def effect_env_fade_out(t):
    return effect_env_none(t) * np.exp(-TWO_PI * t)
