import numpy as np

class Layer:

    def __init__(self):
        self.W = None
        self.B = None
    
    def init_params(self, initializer, m, n):
        return (initializer(m, n), np.zeros((m, n)), np.zeros((m, n)))

    def update_weights(self, dW):
        pass

    def update_biases(self, dB):
        pass

    def forward(self, x):
        pass

    def backward(self, x1, x0, error):
        pass
