import math
import numpy as np
import pandas as pd
#-----------------------------------------------------------------------------------------------------------------------
def load_onefeature_dataset():
    data = np.genfromtxt('../data/data.csv', delimiter=',') # get the data from file
    x = data[:, 0].reshape(-1, 1).copy() # extract the features
    y_true = data[:, 4].copy() # get the true labels
    return x, y_true
#-----------------------------------------------------------------------------------------------------------------------
def load_multifeature_dataset():
    data = np.genfromtxt('../data/data.csv', delimiter=',') # get the data from file
    x = data[:, :4].copy() # extract the features
    y_true = data[:, 4].copy() # get the true labels
    return x, y_true
#-----------------------------------------------------------------------------------------------------------------------
def add_dummy_feature(x): return np.insert(x, 0, np.ones((x.shape[0],)), axis=1)
#-----------------------------------------------------------------------------------------------------------------------
def predict(X, theta): return X @ theta
#-----------------------------------------------------------------------------------------------------------------------
def loss_grad(X, theta, y_true):
    m = X.shape[0]
    errors = predict(X, theta) - y_true
    loss = np.dot(errors, errors) / m
    gradients = (2 / m) * (X.T @ errors)
    return loss, gradients
#-----------------------------------------------------------------------------------------------------------------------
def gradient_descent(X, y_true, num_iter=50, eta=0.1):
    theta = np.zeros(X.shape[1])
    history = []
    for iter in range(num_iter):
        loss, gradients = loss_grad(X, theta, y_true)
        history.append(loss)
        theta = theta - eta * gradients
    return theta, history
#-----------------------------------------------------------------------------------------------------------------------
