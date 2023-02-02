""" Kernel
"""
import json

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import Input, Dense, Embedding, Flatten, Concatenate, Dropout, BatchNormalization
from tensorflow.keras import Sequential, Model

# define documents and labels

with open("data/training.json", encoding="UTF-8") as user_file:
    training = json.load(user_file)
docs1 = np.array([t[0:10] for t in training])
docs2 = np.array([t[10:15] for t in training])
docs3 = np.array([t[15:115] for t in training])
labels1 = np.array([t[115:147] for t in training])

with open("data/validation.json", encoding="UTF-8") as user_file:
    validation = json.load(user_file)
vals1 = np.array([t[0:10] for t in validation])
vals2 = np.array([t[10:15] for t in validation])
vals3 = np.array([t[15:115] for t in validation])
labels2 = np.array([t[115:147] for t in validation])

# define the model

input1 = Sequential([
    Input(shape=(10,))
    ])

input2 = Sequential([
    Embedding(1000, 8, input_length=5),
    Flatten()
    ])

input3 = Sequential([
    Embedding(1000, 32, input_length=100),
    Flatten()
    ])

x = Concatenate()([input1.output, input2.output, input3.output])
x = Dense(768, activation="relu")(x)
x = Dense(128, activation="relu")(x)
output = Dense(32, activation="softmax")(x)
model = Model(inputs=[input1.input, input2.input, input3.input], outputs=output)

# compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# summarize the model

print(model.summary())

while True:
    # fit the model

    model.fit(x=[docs1, docs2, docs3], y=labels1, epochs=50)

    # evaluate the model

    loss, accuracy = model.evaluate(x=[vals1, vals2, vals3], y=labels2, verbose=1)
    print(f"Accuracy: {accuracy*100}")
    if accuracy == 1:
        break

model.save("model")
