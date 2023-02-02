""" Test
"""
import os
os.environ["TF_CPP_MIN_VLOG_LEVEL"] = "3"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import Dense, Embedding, Flatten
from tensorflow.keras.models import Sequential

# define documents

docs = ["Well done!",
        "Good work",
        "Great effort",
        "nice work",
        "Excellent!",
        "not bad work",
        "Weak",
        "Poor effort!",
        "not good",
        "poor work",
        "bad effort",
        "Could have done better."]

# define class labels

labels = np.array([1,1,1,1,1,1,0,0,0,0,0,0])

# integer encode the documents

VOCAB_SIZE = 50
encoded_docs = [one_hot(d, VOCAB_SIZE) for d in docs]
print(encoded_docs)

# pad documents to a max length of 4 words

MAX_LENGTH = 4
padded_docs = pad_sequences(encoded_docs, maxlen=MAX_LENGTH, padding="post")
print(padded_docs)

# define the model

model = Sequential(
        [
            Embedding(VOCAB_SIZE, 8, input_length=MAX_LENGTH),
            Flatten(),
            Dense(1, activation="sigmoid")
            ]
        )

# compile the model
model.compile(
        optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# summarize the model

print(model.summary())

# fit the model

model.fit(padded_docs, labels, epochs=150, verbose=0)

# evaluate the model

loss, accuracy = model.evaluate(padded_docs, labels, verbose=1)
print(f"Accuracy: {accuracy*100}")

# predict a bit

value = input("Please enter a string:\n")
encoded_value = [one_hot(value, VOCAB_SIZE)]
padded_value = pad_sequences(encoded_value, maxlen=MAX_LENGTH, padding="post")
print(f"{padded_value[0]} => {np.squeeze(model.predict(padded_value))}")
