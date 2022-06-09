import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

MAX_SCORE = 15
NB_CHANNELS = 17
NB_CLUSTERS = 3
EFFECTS = ["Increase frequency Touch points", "Improve Reach / Coverage / New prescribers", "PDP evolution Cross-fertilization", "Multiply mode of communication Create a customer journey"]

weights = np.zeros((NB_CHANNELS, MAX_SCORE))
for i in range(0, NB_CHANNELS):
    for j in range(0, MAX_SCORE):
        weights[i][j] = (j + 1)

data = pd.read_csv("data/digital_initiatives_ranking.csv", keep_default_na = False, na_values = False)

# Cluster the countries across their score for each effects

clusters = np.empty((0,8), int)
for effect in EFFECTS:
    where = data["Effect"] == effect
    X = data[where]

    X = X.drop(["Effect", "Score"], axis="columns")
    X = X.pivot(index="Country", columns="Channel", values="NormalizedScore")

    kmeans = KMeans(n_clusters = NB_CLUSTERS)
    kmeans.fit(X)
    y_hat = kmeans.predict(X)
    clusters = np.append(clusters, [y_hat], axis = 0)

# Create the adjacency matrix across their effects and scoring similiraty

adjacency = np.zeros((8, 8), int)
for k in range(0, 4):
    for i in range(0, 8):
        ref = clusters[k][i]
        for j in range(0, 8):
            if i != j and clusters[k][j] == ref:
                adjacency[i][j] = adjacency[i][j] + 1
adjacency = np.vectorize(lambda x: 1 if x >= 2 else 0)(adjacency)

# Draw the graph

G = nx.from_numpy_matrix(np.array(adjacency))  
nx.draw(G, with_labels=True)
#plt.show()

# Found clusters

CLUSTERS = [
    ["Cambodia", "Pakistan"],
    ["Taiwan"],
    ["Bangladesh", "HongKong", "India", "South Korea", "Thailand"]
]

# Compile the results

results = np.zeros((0, NB_CHANNELS), int)
for effect in EFFECTS:
    for cluster in CLUSTERS:
        n = len(cluster)

        where = data["Effect"] == effect
        X = data[where]
        X = X.drop(["Effect", "NormalizedScore"], axis="columns")
        X = X.pivot(index="Country", columns="Channel", values="Score")
        X = X[X.index.isin(cluster)]

        # Calculate the score distributions for each effect and cluster

        distribution = np.zeros((X.columns.shape[0], MAX_SCORE), int)
        i = 0
        for column in X.columns:
            for score in X[column]:
                distribution[i][score - 1] = distribution[i][score - 1] + 1
            i = i + 1
        distribution = np.vectorize(lambda x: x / n)(distribution)

        # Calculate the weighted probability average of each channels

        probability = np.sum(distribution * weights, axis = 1)

        # Add to results

        results = np.append(results, [probability], axis = 0)

data = pd.DataFrame(results.T, columns = ['C1','C2','C3', 'C1', 'C2', 'C3', 'C1', 'C2', 'C3', 'C1', 'C2', 'C3'])
data.to_csv("data/digital_initiatives_ranking_results.csv")
