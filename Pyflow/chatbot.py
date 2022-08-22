import sys
import json
import math

import numpy as np
import nltk as nl

import pyflow as pf

MAX_LENGHT = 10
WORD_SIZE = 8
STOP_WORDS_THRESHOLD = 0.1

def get_idf(stemmatizer, documents):

    # Count occurences of each word in each document

    count = {}
    for document in documents:
        words = set(pf.text.to_words(document))
        words = [stemmatizer.stem(word) for word in words]
        for word in words:
            if not word in count:
                count[word] = 1
            else:
                count[word] += 1
    
    # Return IDF for each word

    idf = {}
    N = len(documents)
    for word in count:
        idf[word] = math.log(N / count[word])
    return idf


def load_data(filename):

    # Load intents data from JSON

    intents = {}
    with open(filename, 'r') as f:
        for intent in json.load(f):
            key = intent["name"]
            intents[key] = intent

    # Extract training data from the intents

    documents = []
    labels = []
    for (name, intent) in intents.items():
        for doc in intent["samples"]:
            documents.append(doc)
            labels.append(name)
    
    return intents, documents, labels


def build_model(intents, documents, labels):
    
    # Build a dictionary of all unique non stop words from the documents
    # A stop word is a word with idf ~= 0 (apperaing in almost all documents)

    stemmatizer = nl.stem.PorterStemmer()
    idf = get_idf(stemmatizer, documents)
    dictionary = [word for word in idf if idf[word] > STOP_WORDS_THRESHOLD]
    
    # Build a list of all unique labels
    
    classes = sorted(list(set(labels)))
   
    # Compile a neural network model

    model = pf.Model([
        pf.Embedding(len(dictionary) + 1, WORD_SIZE),
        pf.Dense(MAX_LENGHT * WORD_SIZE, 64, activation='relu'),
        pf.Dense(64, len(classes), activation = 'softmax')
    ])
    model.compile(optimizer = 'adam', loss = 'cce') 
   
    # Some helpers to use the model

    h = lambda w: pf.text.hash_with_dict(dictionary, stemmatizer.stem(w))
    o = lambda d: pf.text.one_hot(d, hash_func=h)
    O = lambda D: [o(d) for d in D]
    x = lambda d: np.array(pf.text.pad_sequences([o(d)], maxlen = MAX_LENGHT))
    X = lambda D: np.array(pf.text.pad_sequences(O(D), maxlen = MAX_LENGHT))
    Y = lambda L: np.array(pf.text.to_categoricals(L, classes))

    # Return fit and predit functions

    fit = lambda d, l: model.fit(X(d), Y(l), epochs = 150, verbose = True)
    predict = lambda d: intents[classes[np.argmax(model.predict(x(d)))]]
    return fit, predict


def get_random_answer(intent):
    if intent is None:
        return "ok, let continue!"
    else:
        answers = intent["answers"]
        n = len(answers)
        p = np.random.randint(0, n)
        return answers[p]


def is_done(intent):
    return intent is not None and intent["name"] == "bye"


def create_assistant(filename):
    
    # Load and train the model

    intents, documents, labels = load_data(filename)
    train, listen = build_model(intents, documents, labels)
    train(documents, labels)

    # Return the assistant

    reply = lambda args: (args[0], is_done(args[1]), get_random_answer(args[1]))
    talk = lambda act, context, input_: reply(act(context, listen(input_)))
    return lambda act: lambda context, input_: talk(act, context, input_)


def act(context, intent):
    if intent["name"] == "bye":
        print("Are you sure?")
        cin = input("# ").lower()
        if cin == "y" or cin == "yes":
            return context, intent
        else:
            return context, None
    else:
        return context, intent


def main():
    assistant = create_assistant("data/intents.json")(act)

    context = None
    done = False
    while not done:
        user_input = input("# ")
        context, done, message = assistant(context, user_input)
        print(message)


if __name__ == "__main__":
    np.random.seed(42)
    sys.exit(main())
