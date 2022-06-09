import os
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np

from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding

# define documents

docs = ['Well done!',
		'Good work',
		'Great effort',
		'nice work',
		'Excellent!',
        'not bad work',
		'Weak',
		'Poor effort!',
		'not good',
		'poor work',
        'bad effort',
		'Could have done better.']

# define class labels

labels = np.array([1,1,1,1,1,1,0,0,0,0,0,0])

# integer encode the documents

vocab_size = 50
encoded_docs = [one_hot(d, vocab_size) for d in docs]
print(encoded_docs)

# pad documents to a max length of 4 words

max_length = 4
padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
print(padded_docs)

# define the model

model = Sequential(
    [
        Embedding(vocab_size, 8, input_length=max_length),
        Flatten(),
        Dense(1, activation='sigmoid')
    ]
)

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# summarize the model

print(model.summary())

# fit the model

model.fit(padded_docs, labels, epochs=150, verbose=0)

# evaluate the model

loss, accuracy = model.evaluate(padded_docs, labels, verbose=1)
print('Accuracy: %f' % (accuracy*100))

# predict a bit

value = input("Please enter a string:\n")
encoded_value = [one_hot(value, vocab_size)]
padded_value = pad_sequences(encoded_value, maxlen=max_length, padding='post')
print("%s => %s" % (padded_value[0], np.squeeze(model.predict(padded_value))))
