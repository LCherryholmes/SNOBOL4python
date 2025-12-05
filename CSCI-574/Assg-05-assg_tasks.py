import math
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

def task_1_1_load_data():
    X = pd.read_csv("../data/assg-05-data1.csv", header=None, names=['x_1', 'x_2', 'y'])
    y = X['y'].to_numpy()
    X = X.drop(columns='y')
    return X, y

def task_1_2_linear_svm_classifier(X, y, C=1.0):
    model = Pipeline([
        ('ss', StandardScaler()),
        ('svc', SVC(kernel="linear", C=C))
        ])
    model.fit(X, y)
    return model

def gaussian_kernel(xi, xj, sigma):
    x_diff = xi - xj
    return math.exp(-np.dot(x_diff, x_diff) / (2.0 * sigma * sigma))

def task_3_1_load_data():
    X = pd.read_csv("../data/assg-05-data2.csv", header=None, names=['x_1', 'x_2', 'y'])
    y = X['y'].to_numpy()
    X = X.drop(columns='y')
    return X, y

def task_3_2_rbf_svm_classifier(X, y, kernel='rbf', C=1.0, gamma=8.0):
    model = Pipeline([
        ('ss', StandardScaler()),
        ('svc', SVC(kernel=kernel, C=C, gamma=gamma))
        ])
    model.fit(X, y)
    return model
