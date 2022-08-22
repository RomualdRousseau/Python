import math
import numpy as np

from .util import *
from .functions import _functions
from .Layer import Layer

class Dense(Layer):

    def __init__(self, units, outputs, activation = 'linear', 
            kernel_initializer = 'gorot', bias_initializer = 'zeros'):
        super().__init__()

        self.activation = _functions[activation]['func']
        self.activation_prime = _functions[activation]['prime']
        self.kernel_initializer = _functions[kernel_initializer]['func']
        self.bias_initializer = _functions[bias_initializer]['func']

        self.W = self.init_params(self.kernel_initializer, units, outputs)
        self.B = self.init_params(self.bias_initializer, 1, outputs)

    def update_weights(self, dW):
        self.W = (self.W[0] + dW[0], dW[1], dW[2])

    def update_biases(self, dB):
        self.B = (self.B[0] + dB[0], dB[1], dB[2])

    def forward(self, x):
        return self.activation(x @ self.W[0] + self.B[0])

    def backward(self, x1, x0, error):
        error = error * self.activation_prime(x1)
        dW = x0.T @ error
        dB = error.sum(axis=0, keepdims=True)
        error = error @ self.W[0].T
        return dW, dB, error
