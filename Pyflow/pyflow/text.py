import numpy as np

def hash_auto(w, n): 
    return hash(w) % (n - 1) + 1

def hash_with_dict(dictionary, w):
    try:
        return dictionary.index(w) + 1
    except ValueError:
        return 0

def to_categoricals(labels, classes):
    return [np.take(np.eye(len(classes)), classes.index(l), axis=0) for l in labels]

def to_words(input_text, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', split=' '):
    cleaned_text = ''.join((filter(lambda x: x not in filters, input_text)))
    cleaned_text = cleaned_text.lower()
    cleaned_text = cleaned_text.split(split)
    return cleaned_text

def one_hot(input_text, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', split=' ', hash_func=hash_auto):
    return [hash_func(w) for w in to_words(input_text, filters, split)]

def pad_sequences(sequences, maxlen, value=0):
    return [[(s[i] if i < len(s) else value) for i in range(maxlen)] for s in sequences]

def all_words(documents, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', split=' '):
    return list(set([w for d in documents for w in to_words(d, filters, split)]))

def corr(data, words, hash_func=hash_auto):
    mask = [hash_func(w) for w in words]
    res = data[mask]
    return np.corrcoef(res)
