import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt

import pyflow as pf

NUMBER_OF_DATA_POINTS = 100
POLY_DEGREE_INPUT = 8
POLY_DEGREE_OUTPUT = 1
                                                                                                                        
poly_kernel = lambda x, n: np.array([x ** (k + 1) for k in range(n)])


def mapv(x, a1, b1, a2, b2):                                                                                            
    t = (b2 - a2) / (b1 - a1) if a1 != a2 else 0
    return (x - a1) * t + a2


def main():
    np.random.seed(42)

    # Generate sample fo data points; sinusoid with noise                                                               
    
    X_train = np.linspace(-1, 1, NUMBER_OF_DATA_POINTS)                                                             
    Y_train = 0.95 * np.sin(X_train * 8) + 0.05 * np.random.uniform(-1, 1, NUMBER_OF_DATA_POINTS)
    X_train = np.array([poly_kernel(x, POLY_DEGREE_INPUT) for x in X_train])
    Y_train = Y_train.reshape(-1, POLY_DEGREE_OUTPUT)

    model = pf.Model([
        pf.Dense(POLY_DEGREE_INPUT, POLY_DEGREE_OUTPUT)
    ])
    model.compile(optimizer = 'adadelta', loss = 'mse')

    history = model.fit(X_train, Y_train, epochs = 50000)
    Y_test = model.predict(X_train)

    plt.plot(Y_train)
    plt.plot(Y_test)
    plt.show()


if __name__ == "__main__":
    sys.exit(main())
