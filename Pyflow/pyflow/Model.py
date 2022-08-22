import math
import numpy as np

from .util import *
from .functions import _functions


class Model:

    def __init__(self, layers, write_mask = None):
        self.layers = layers
        self.write_mask = [True] * len(layers) if write_mask is None else write_mask
    
    def predict(self, x):
        xhat, yhat = self._forward(x)
        return yhat

    def fit(self, x, y, epochs = 10, batch_size = 128, shuffle = True, verbose = True):
        N = x.shape[0]

        history = {
            'train_loss': [],
            'train_accuracy': []
        }

        batch_sample = np.arange(N)
        batch_count = math.ceil(N / batch_size)

        first_pass = True

        for e in range(1, 1 + epochs):

            if verbose:
                print(f"Epoch {e}/{epochs}")

            if shuffle:
                np.random.shuffle(batch_sample)

            train_loss = 0
            train_accuracy = 0
            
            for i in range(batch_count):
                batch_x = x[batch_sample[i * batch_size : (i + 1) * batch_size]]
                batch_y = y[batch_sample[i * batch_size : (i + 1) * batch_size]]
            
                _, _, loss, accuracy = self._call(batch_x, batch_y, True)
                train_loss += loss / batch_count
                train_accuracy += accuracy / batch_count

                if first_pass:
                    first_pass = False
                    history['train_loss'].append(loss)
                    history['train_accuracy'].append(accuracy)
            
                if verbose:
                    beta = (i + 1) / batch_count
                    bar = "=" * int(30 * beta) + ">" + "." * int(30 * (1 - beta))
                    print(f"{i:3d}/{batch_count} [{bar}]\r", end='')

            history['train_loss'].append(train_loss)
            history['train_accuracy'].append(train_accuracy)

            if verbose:
                bar = "=" * 30
                print(f"{batch_count}/{batch_count} [{bar}] - loss: {train_loss:.4f} - accuracy: {train_accuracy:.4f}")

        return history

    def evaluate(self, x, y, verbose = True):
        _, yhat, loss, accuracy = self._call(x, y, False)

        if verbose:
            print(f"Test loss: {loss}")
            print(f"Test accuracy: {accuracy}")

        return loss, accuracy, yhat

    def compile(self, optimizer = 'rmsprop', loss = 'mse'):
        self._optimizer = _functions[optimizer]['func']
        self._loss_func =  _functions[loss]['func']
        self._loss_prime =  _functions[loss]['prime']
        self._loss_acc =  _functions[loss]['acc']

        def forward(layers, result):
            if not layers:
                return result, result[-1]
            else:
                head, *tail = layers
                return forward(tail, result + [ head.forward(result[-1]) ])

        def backward(layers, x, error, result):
            if not layers:
                return result
            else:
                *head, tail = layers
                dW, dB, error = tail.backward(x[-1], x[-2], error)
                return backward(head, x[:-1], error, [(dW, dB)] + result)

        def update(optimizer, layers, write_mask, weights):
            if not layers:
                pass
            else:
                head, *tail = layers
                if write_mask[0]:
                    head.update_weights(optimizer(weights[0][0], head.W[1], head.W[2]))
                    if head.B is not None:
                        head.update_biases(optimizer(weights[0][1], head.B[1], head.B[2]))
                update(optimizer, tail, write_mask[1:], weights[1:])
                 
        def call_without_training(x, y):
            xhat, yhat = self._forward(x)
            return xhat, yhat, self._loss_func(y, yhat).mean(), self._loss_acc(y, yhat).mean()

        def call_with_training(x, y):
            xhat, yhat, loss, accuracy = call_without_training(x, y)
            self._update(self._backward(xhat, self._loss_prime(y, yhat)))
            return xhat, yhat, loss, accuracy
        
        self._forward = lambda x: forward(self.layers, [x])
        self._backward = lambda x, e : backward(self.layers, x, e, [])
        self._update = lambda w: update(self._optimizer, self.layers, self.write_mask, w)
        self._call = lambda x, y, training: call_with_training(x, y) if training else call_without_training(x, y)
