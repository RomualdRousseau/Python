from .util import *


_functions = {
        'linear': {
            'func': ac_lin,
            'prime': ac_lin_prime
        },
        'sigmoid': {
            'func': ac_sigmoid,
            'prime': ac_sigmoid_prime
        },
        'tanh': {
            'func': ac_tanh,
            'prime': ac_tanh_prime
        },
        'relu': {
            'func': ac_relu,
            'prime': ac_relu_prime
        },
        'leaky_relu': {
            'func': ac_leaky_relu,
            'prime': ac_leaky_relu_prime
        },
        'softmax': {
            'func': ac_softmax,
            'prime': ac_softmax_prime
        },
        'cce': {
            'func': lo_cce,
            'prime': lo_cce_prime,
            'acc': lambda y, yhat: np.argmax(y, axis=1) == np.argmax(yhat, axis=1)
        },
        'bce': {
            'func': lo_bce,
            'prime': lo_bce_prime,
            'acc': lambda y, yhat: np.clip(1.0 - lo_bce(y, yhat), 0.0, 1.0) 
        },
        'mse': {
            'func': lo_mse,
            'prime': lo_mse_prime,
            'acc': lambda y, yhat: np.clip(1.0 - lo_mse(y, yhat), 0.0, 1.0)
        },
        'zeros': {
            'func': wi_zeros
        },
        'gorot': {
            'func': wi_gorot
        },
        'he': {
            'func': wi_he
        },
        'adadelta': {
            'func': wu_adadelta
        },
        'rmsprop': {
            'func': wu_rmsprop
        },
        'adam': {
            'func': wu_adam
        }
    }
