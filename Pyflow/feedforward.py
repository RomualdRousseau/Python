import sys
import numpy as np
import matplotlib.pyplot as plt

import pyflow as pf


def plt_draw_images(plt, images, labels, m, n):
    splt = plt.subplots(m, n)
    for i in range(m):
        for j in range(n):
            splt[i, j].set_title("label = %d" % np.argmax(labels[i * n + j]))
            splt[i, j].imshow(images[i * n + j].reshape(28, 28), cmap='gray')
            splt[i, j].set(xticks=[], yticks=[])


def plt_draw_graph(plt, history):
    splt = plt.gca()
    splt.set_title('Accuracies and Losses')
    splt.plot(history['train_accuracy'], 'g', label='Accuracy')
    splt.plot(history['train_loss'], 'b', label='Loss')
    splt.legend()


def main():
    np.random.seed(42)

    X_train, Y_train = pf.load_mnist_train_data()
    X_test, Y_test = pf.load_mnist_test_data()

    print("%d train samples" % (X_train.shape[0]))
    print("%d test samples" % (X_test.shape[0]))

    model = pf.Model([
        pf.Dense(784, 128, activation = 'tanh', kernel_initializer = 'gorot'),
        pf.Dense(128, 10, activation = 'softmax', kernel_initializer = 'gorot')
    ])
    model.compile(optimizer = 'adam', loss = 'cce')

    history = model.fit(X_train, Y_train, epochs = 20)
    model.evaluate(X_test, Y_test)

    root = plt.figure(constrained_layout=True)
    div1 = root.subfigures(2, 1)
    plt_draw_graph(div1[0], history)
    plt_draw_images(div1[1], X_test, Y_test, 4, 8)
    plt.show()


if __name__ == "__main__":
    sys.exit(main())
