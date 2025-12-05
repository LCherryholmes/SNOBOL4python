import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
#-----------------------------------------------------------------------------------------------------------------------
def task1_load_data():
    data = pd.read_csv("../data/assg-03-data.csv")
    X = data.x.to_numpy().reshape(-1, 1)
    y = data.y.to_numpy()
    return X, y
#-----------------------------------------------------------------------------------------------------------------------
def task2_underfit_model(x, y):
    pipeline = Pipeline(
        [ ('PolynomialFeatures', PolynomialFeatures(degree=2, include_bias=False))
        , ('LinearRegression', LinearRegression())
        ])
    return pipeline.fit(x, y)
#-----------------------------------------------------------------------------------------------------------------------
def task3_learning_curve_errors(model, X, y):
    train_errors = []
    test_errors = []
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    for size in range(1, len(X_train)):
        X_chunk = X_train[:size]
        y_chunk = y_train[:size]
        model.fit(X_chunk, y_chunk)
        y_chunk_pred = model.predict(X_chunk)
        y_test_pred = model.predict(X_test)
        train_errors.append(root_mean_squared_error(y_chunk, y_chunk_pred))
        test_errors.append(root_mean_squared_error(y_test, y_test_pred))
    return train_errors, test_errors
#-----------------------------------------------------------------------------------------------------------------------
def task4_overfit_model(x, y):
    pipeline = Pipeline(
        [ ('PolynomialFeatures', PolynomialFeatures(degree=100, include_bias=False))
        , ('LinearRegression', LinearRegression())
        ])
    return pipeline.fit(x, y)
#-----------------------------------------------------------------------------------------------------------------------
def task5_lasso_model(x, y, alpha=0.005):
    pipeline = Pipeline(
        [ ('PolynomialFeatures', PolynomialFeatures(degree=100, include_bias=False))
        , ('Lasso', Lasso(alpha=alpha))
        ])
    return pipeline.fit(x, y)
#-----------------------------------------------------------------------------------------------------------------------
def task6_ridge_model(x, y):
    pipeline = Pipeline(
        [ ('PolynomialFeatures', PolynomialFeatures(degree=100, include_bias=False))
        , ('Ridge', Ridge(alpha=0.005, solver="cholesky")) # 0.016
        ])
    return pipeline.fit(x, y)
#-----------------------------------------------------------------------------------------------------------------------
