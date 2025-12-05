import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#=======================================================================================================================
def task_1_1_load_data():
    df = pd.read_csv("../data/assg-07-data-kmeans.csv", header=None)
    return df.to_numpy()
#=======================================================================================================================
def find_closest_centroids(X, centroids):
    labels = []
    for x in X:
        distances = []
        for c in centroids:
            diff = x - c
            distance = np.dot(diff, diff)
            distances.append(distance)
        labels.append(np.argmin(distances))
    return np.array(labels)
#-----------------------------------------------------------------------------------------------------------------------
def find_closest_centroids(X, centroids):
    distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2) ** 2
    return np.argmin(distances, axis=1)
#-----------------------------------------------------------------------------------------------------------------------
def find_closest_centroids(X, centroids):
    distances = np.sum((X[:, np.newaxis, :] - centroids[np.newaxis, :, :]) ** 2, axis=2)
    return np.argmin(distances, axis=1)
#=======================================================================================================================
def compute_centroids(X, c, K):
    centroids = []
    for k in range(0, K):
        Xc = X[c == k]
        centroids.append(Xc.sum(axis=0) / Xc.shape[0])
    return np.array(centroids)
#-----------------------------------------------------------------------------------------------------------------------
def compute_centroids(X, c, K):
    centroids = np.zeros((K, X.shape[1]))
    counts = np.zeros(K)
    np.add.at(centroids, c, X)
    np.add.at(counts, c, 1)
    centroids /= counts[:, None]
    return centroids
#=======================================================================================================================
def kmeans_cluster(X, K, num_iter=10, random_state=42):
    np.random.seed(random_state)
    m = X.shape[0]
    indices = np.random.choice(m, size=K, replace=False)
    centroids = X[indices]
    history = []
    history.append(centroids.copy())
    for i in range(0, num_iter):
        labels = find_closest_centroids(X, centroids)
        centroids = compute_centroids(X, labels, K)
        history.append(centroids.copy())
    return labels, history
#=======================================================================================================================
def task_2_1_load_data():
    df = pd.read_csv("../data/assg-07-data-pca.csv", header=None)
    return df.to_numpy()
#=======================================================================================================================
from sklearn.preprocessing import StandardScaler
def feature_normalize(X):
    std_scaler = StandardScaler()
    X_scaled = std_scaler.fit_transform(X)
    mu = std_scaler.mean_
    sigma = std_scaler.scale_
    return X_scaled, mu, sigma
#-----------------------------------------------------------------------------------------------------------------------
def feature_normalize(X):
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    X_scaled = (X - mu) / sigma
    return X_scaled, mu, sigma
#=======================================================================================================================
from sklearn.decomposition import PCA
def pca(X):
    X_scaled, mu, sigma = feature_normalize(X)
    pca = PCA(n_components=2)
    pca.fit(X_scaled)
    U = pca.components_
    for i in range(U.shape[0]):
        if U[i, 0] > 0:
            U[i, :] = -U[i, :]    
    S = pca.explained_variance_
    return U, S, mu, sigma
#-----------------------------------------------------------------------------------------------------------------------
def pca(X):
    X_scaled, mu, sigma = feature_normalize(X)
    U, s, Vt = np.linalg.svd(X_scaled, full_matrices=False)
    m = X_scaled.shape[0]
    explained_variance = (s ** 2) / m
    U = Vt.T
    for i in range(U.shape[0]):
        if U[i, 0] > 0:
            U[i, :] = -U[i, :]    
    return U, explained_variance, mu, sigma
#=======================================================================================================================
def project_data(X, U, K):
    return X @ U[:, :K]
#=======================================================================================================================
def recover_data(Z, U):
    K = 1
    return Z @ U[:, :K].T
#=======================================================================================================================
