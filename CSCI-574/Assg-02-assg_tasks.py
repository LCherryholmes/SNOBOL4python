import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import make_pipeline

def task1_sklearn_linear_regression(X, y):
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    intercept = model.intercept_
    slope = model.coef_[0]
    MSE = mean_squared_error(y, y_pred)
    RMSE = np.sqrt(MSE)
    rsquared = r2_score(y, y_pred)
    return model, intercept, slope, MSE, RMSE, rsquared

def task1_statsmodel_linear_regression(y, X):
    x = sm.add_constant(X)
    model = sm.OLS(y, x)
    results = model.fit()
    intercept = results.params[0]
    slope = results.params[1]
    MSE = np.mean(results.resid ** 2)
    RMSE = np.sqrt(MSE)
    rsquared = results.rsquared
    return results, intercept, slope, MSE, RMSE, rsquared

def task2_label_encoding(df_rain_tomorrow):
    rain_tomorrow = df_rain_tomorrow.to_numpy().reshape(-1,1)
    pipeline = make_pipeline(OrdinalEncoder())
    y = pipeline.fit_transform(rain_tomorrow).reshape(-1)
    ndim = y.ndim
    shape = y.shape
    num_no = (y == 0.0).sum()
    num_yes = (y == 1.0).sum()
    return y, ndim, shape, num_no, num_yes

def task2_impute_missing_data(df):
    imputer = SimpleImputer(strategy="mean")
    sunshine = df.Sunshine.to_numpy().reshape(-1,1)
    sunshine = imputer.fit_transform(sunshine)
    result = pd.DataFrame({'Sunshine': sunshine.reshape(-1), 'Pressure3pm': df.Pressure3pm})
    return result, result.ndim, result.shape, result.columns, result.isna().sum()

def task2_sklearn_logistic_regression(X, y):
    model = LogisticRegression(solver='lbfgs', C=500.0)
    model.fit(X, y)
    y_pred = model.predict(X)
    intercept = model.intercept_[0]
    slopes = model.coef_[0]
    accuracy = accuracy_score(y, y_pred)
    return model, intercept, slopes, accuracy

def task2_statsmodel_logistic_regression(y, X):
    x = sm.add_constant(X)
    model = sm.Logit(y, x)
    results = model.fit()
    intercept = results.params.iloc[0]
    slopes = results.params.iloc[1:]
    y_pred = (results.predict(x) > 0.5).astype(int)
    accuracy = np.mean(y == y_pred)
    return results, intercept, slopes, accuracy