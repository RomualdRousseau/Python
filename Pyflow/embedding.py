import sys
import numpy as np
import matplotlib.pyplot as plt

import pyflow as pf

VOCAB_SIZE = 50
MAX_LENGHT = 4
WORD_SIZE = 8

docs = ['Well done!',
        'Good work',
        'Great effort',
        'nice work',
        'Excellent!',
        'very good',
        'Weak',
        'Poor effort!',
        'poor work',
        'bad effort',
        'Could have done better.',
        'very bad']

labels = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]).reshape((-1, 1))



def plt_draw_matrix(plt, matrix):
    plt.matshow(matrix, cmap = "Blues_r")
    for tick in plt.get_xticklabels():
        tick.set_rotation(90)


def main():
    np.random.seed(42)

    all_words = sorted(pf.text.all_words(docs))
    
    h = lambda w: pf.text.hash_with_dict(all_words, w)

    padded_docs = np.array(pf.text.pad_sequences([pf.text.one_hot(d, hash_func=h)
                                for d in docs], maxlen=MAX_LENGHT))

    model = pf.Model([
        pf.Embedding(len(all_words) + 1, WORD_SIZE),
        pf.Dense(MAX_LENGHT * WORD_SIZE, 64, activation = 'relu'),
        pf.Dense(64, 1, activation = 'sigmoid')
    ])
    model.compile(optimizer = 'adam', loss = 'mse') 

    corr_matrix_before = pf.text.corr(model.layers[0].H[0], all_words, hash_func=h)

    model.fit(padded_docs, labels, epochs = 2000)

    corr_matrix_after = pf.text.corr(model.layers[0].H[0], all_words, hash_func=h)
    corr_words_after = sorted(
        all_words, key=lambda w: corr_matrix_after[all_words.index("good")][all_words.index(w)], reverse=True)
    corr_matrix_after = pf.text.corr(model.layers[0].H[0], corr_words_after, hash_func=h)

    print(padded_docs)

    x = np.array(pf.text.pad_sequences([pf.text.one_hot("bad", hash_func=h)], maxlen=MAX_LENGHT))
    y = model.predict(x)
    print(x[0], y[0])

    fig, div1 = plt.subplots(1, 2, sharex = True, sharey = True)
    plt_draw_matrix(div1[0], corr_matrix_before)
    plt_draw_matrix(div1[1], corr_matrix_after)
    plt.xticks(range(len(corr_words_after)), corr_words_after)
    plt.yticks(range(len(corr_words_after)), corr_words_after)
    plt.show()


if __name__ == "__main__":
    sys.exit(main())
