import math
import numpy as np


def ac_lin(x):
    return x

def ac_lin_prime(y): 
    return 1.0


def ac_tanh(x):
    return np.tanh(x)

def ac_tanh_prime(y): 
    return 1.0 - y**2


def ac_sigmoid(x):
    return np.exp(-np.logaddexp(0, -x))
    #return np.where(x >= 0, 
    #    1.0 / (1.0 + np.exp(-x)), 
    #    np.exp(x) / (1.0 + np.exp(x)))
    #return (1.0 + np.exp(-x))**-1

def ac_sigmoid_prime(y): 
    return y * (1.0 - y)


def ac_relu(x):
    return np.where(x <= 0.0, 0.0, x)

def ac_relu_prime(y):
    return np.where(y == 0.0, 0.0, 1.0)


def ac_leaky_relu(x, a = 0.1):
    return np.where(x <= 0.0, a * x, x)

def ac_leaky_relu_prime(y, a = 0.1):
    return np.where(y == 0.0, a, 1.0)


def ac_softmax(x):
    max = np.max(x, axis=1, keepdims=True)
    e_x = np.exp(x - max)
    sum = np.sum(e_x, axis=1, keepdims=True)
    return e_x / sum

def ac_softmax_prime(y):
    return y * (1.0 - y)


def lo_mse(x1, x2): 
    return 0.5 * (x1 - x2) ** 2

def lo_mse_prime(x1, x2): 
    return (x2 - x1) / x2.shape[0]


def lo_cce(x1, x2):
    return -x1 * np.log(x2)

def lo_cce_prime(x1, x2):
    return (x2 - x1) / x2.shape[0]


def lo_bce(x1, x2):
    return -(x1 * np.log(x2) + (1.0 - x1) * np.log(1.0 - x2))

def lo_bce_prime(x1, x2):
    return ((x2 - x1) / (x2 * (1.0 - x2))) / x2.shape[0]


def lr_exp_decay(e): 
    return max(0.01 * np.exp(-0.95 * e), 0.001)


def wi_zeros(n, m):
    return np.zeros((n, m)).astype(np.float32)


def wi_gorot(n, m):
    a = math.sqrt(6.0 / (n + m))
    return np.random.uniform(-a, a, size=(n,m)).astype(np.float32)


def wi_he(n, m):
    a = math.sqrt(6.0 / n)
    return np.random.uniform(-a, a, size=(n,m)).astype(np.float32)


def wu_adadelta(W, S, V, rho = 0.95):
    S = rho * S + (1.0 - rho) * W**2
    X = -W * np.sqrt(V + 1e-6) / np.sqrt(S + 1e-6)
    V = rho * V + (1.0 - rho) * X**2
    return (X, S, V)


def wu_rmsprop(W, S, V, rho = 0.9, lr = 0.001):
    S = rho * S + (1.0 - rho) * W**2
    X = -W * lr / np.sqrt(S + 1e-6)
    return (X, S, V)


def wu_adam(W, S, V, beta1 = 0.9, beta2 = 0.999, lr = 0.001):
    S = beta1 * S + (1.0 - beta1) * W
    V = beta2 * V + (1.0 - beta2) * W**2
    Shat = S / (1.0 - beta1)
    Vhat = V / (1.0 - beta2)
    X = -Shat * lr / np.sqrt(Vhat + 1e-8)
    return (X, S, V)


def to_categoricals(labels, num_classes):
    return [np.take(np.eye(num_classes), l, axis=0) for l in labels]
