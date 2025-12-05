import math
import numpy as np

def basic_sigmoid(x): return 1.0 / (1.0 + math.exp(-x))
def sigmoid(x): return 1.0 / (1.0 + np.exp(-x))
def sigmoid_grad(x): s = sigmoid(x); return s * (1.0 - s)
def standard_scalar(x): μ = x.mean(axis=0); σ = x.std(axis=0); return (x - μ) / σ, μ, σ
def softmax(x): e = np.exp(x); return e / np.sum(e, axis=1, keepdims=True)
def one_hot(category):
    glossary = {val: idx for idx, val in enumerate(np.unique(category))}
    indices = np.array([glossary[val] for val in category])
    onehot = np.zeros((len(category), len(glossary)), dtype=int)
    onehot[np.arange(len(category)), indices] = 1.0
    return onehot
def mae(y_pred, y_true): return np.sum(np.abs(y_pred - y_true)) / y_true.shape[0]
def rmse(y_pred, y_true):
    y_diff = y_pred - y_true
    return math.sqrt(np.dot(y_diff, y_diff) / y_true.shape[0])
