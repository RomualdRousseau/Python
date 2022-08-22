import math
import numpy as np

from .util import *
from .functions import _functions
from .Layer import Layer

class Embedding(Layer):

    def __init__(self, vocab_size, word_size, kernel_initializer = 'gorot'):
        super().__init__()

        self.kernel_initializer = _functions[kernel_initializer]['func']

        self.H = self.init_params(self.kernel_initializer, vocab_size, word_size)
        self.H[0][0] = 0

    def update_weights(self, dW):
        self.H[0][self.inputs] = self.W[0] + dW[0]
        self.H[1][self.inputs] = dW[1]
        self.H[2][self.inputs] = dW[2]

    def forward(self, x):
        self.inputs = x
        self.W = (self.H[0][x], self.H[1][x], self.H[2][x]) 
        return self.W[0].reshape((-1, x.shape[1] * self.H[0].shape[1]))

    def backward(self, x1, x0, error):
        error = error.reshape((-1, x0.shape[1], self.H[0].shape[1]))
        dW = np.where(x0 > 0, 1, 0).reshape(-1, x0.shape[1], 1) * error
        error = (error * self.W[0]).reshape((-1, x0.shape[1] * self.H[0].shape[1]))
        return dW, None, error
