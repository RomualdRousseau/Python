import struct as st
import numpy as np


def _load_ubyte_data(images_filename, labels_filename):
    with open(images_filename,'rb') as file:
        file.seek(0)
        magic = st.unpack('>4B', file.read(4))
        n_i = st.unpack('>I', file.read(4))[0] #num of images
        n_r = st.unpack('>I', file.read(4))[0] #num of rows
        n_c = st.unpack('>I', file.read(4))[0] #num of column
        n_tot = n_i * n_r * n_c
        data = np.asarray(
                st.unpack('>' + 'B' * n_tot, file.read(n_tot))
                ).reshape((n_i, n_r * n_c))

    with open(labels_filename,'rb') as file:
        file.seek(0)
        magic = st.unpack('>4B', file.read(4))
        n_i = st.unpack('>I', file.read(4))[0] #num of images
        n_tot = n_i
        labels = np.asarray(
                st.unpack('>' + 'B' * n_tot, file.read(n_tot))
                )
        targets = np.zeros((labels.shape[0], 10))
        targets[range(labels.shape[0]), labels] = 1

    return data.astype("float32") / 255.0, targets.astype("float32")


def load_mnist_train_data():
    return _load_ubyte_data(
            'data/train-images-idx3-ubyte', 
            'data/train-labels-idx1-ubyte')


def load_mnist_test_data():
    return _load_ubyte_data(
            'data/t10k-images-idx3-ubyte', 
            'data/t10k-labels-idx1-ubyte')
