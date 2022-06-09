import sys
import numpy as np
import matplotlib.pyplot as plt

import pyflow as pf


def plt_draw_images(plt, images, labels, m, n):
    splt = plt.subplots(m, n)
    for i in range(m):
        for j in range(n):
            if labels is not None:
                splt[i, j].set_title("label = %d" % np.argmax(labels[i * n + j]))
            splt[i, j].imshow(images[i * n + j].reshape(28, 28), cmap='gray')
            splt[i, j].set(xticks=[], yticks=[])


def plt_draw_graph(plt, history):
    splt = plt.subplots()
    splt.set_title('Accuracies and Losses')
    splt.plot(history['train_accuracy'], 'g', label='Accuracy')
    splt.plot(history['train_loss'], 'b', label='Loss')
    splt.legend()


def main():
    np.random.seed(42)

    X_train, Y_train = pf.load_mnist_train_data()
    X_test, Y_test = pf.load_mnist_test_data()

    encoder = pf.Model([
        pf.Dense(784, 128, activation = 'relu', kernel_initializer = 'he'),
        pf.Dense(128, 32, activation = 'relu', kernel_initializer = 'he'),
    ])
    encoder.compile(optimizer = 'adam', loss = 'bce')

    decoder = pf.Model([
        pf.Dense(32, 128, activation = 'relu', kernel_initializer = 'he'),
        pf.Dense(128, 784, activation = 'sigmoid', kernel_initializer = 'gorot')
    ])
    decoder.compile(optimizer = 'adam', loss = 'bce')

    autoencoder = pf.Model(encoder.layers + decoder.layers)
    autoencoder.compile(optimizer = 'adam', loss = 'bce')
    
    history = autoencoder.fit(X_train, X_train, epochs = 25)
    _, _, yhat = autoencoder.evaluate(X_test, X_test)

    X_random = np.array([np.random.uniform(0, 5, 32) for i in range(4 * 4)])
    yhat2 = decoder.predict(X_random)

    model = pf.Model(encoder.layers + [
        pf.Dense(32, 784, activation = 'tanh', kernel_initializer = 'gorot'),
        pf.Dense(784, 10, activation = 'softmax', kernel_initializer = 'gorot')
    ], [False, False, True, True])
    model.compile(optimizer = 'adam', loss = 'cce')

    history2 = model.fit(X_train, Y_train, epochs = 100)
    model.evaluate(X_test, Y_test)

    root = plt.figure(constrained_layout=True)
    div1 = root.subfigures(2, 1)
    plt_draw_graph(div1[0], history)
    div2 = div1[1].subfigures(1, 3)
    plt_draw_images(div2[0], X_test, Y_test, 4, 4)
    plt_draw_images(div2[1], yhat, Y_test, 4, 4)
    plt_draw_images(div2[2], yhat2, None, 4, 4)
    plt.show()


if __name__ == "__main__":
    sys.exit(main())
