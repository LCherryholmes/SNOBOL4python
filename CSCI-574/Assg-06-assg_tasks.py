import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_openml
#-----------------------------------------------------------------------------------------------------------------------
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
#-----------------------------------------------------------------------------------------------------------------------
def task_1_load_data():
    magic_telescope = fetch_openml(data_id=1120, as_frame=True) # "MagicTelescope" # 43971
    X = pd.DataFrame(magic_telescope.data, columns=magic_telescope.feature_names)
    y = magic_telescope.target.to_numpy() == 'g'
    return X, y
#-----------------------------------------------------------------------------------------------------------------------
def train_val_test_split(data, target, train_size=10000, val_size=4510, random_state=42):
    total_size = data.shape[0]
    remaining_size = total_size - train_size
    X_train, X_rest, y_train, y_rest = \
        train_test_split(data, target, train_size=train_size, test_size=remaining_size, random_state=random_state)
    X_val, X_test, y_val, y_test = \
        train_test_split(X_rest, y_rest, train_size=val_size, test_size=remaining_size-val_size, random_state=random_state)
    return (X_train, y_train, X_val, y_val, X_test, y_test)
#-----------------------------------------------------------------------------------------------------------------------
def task_3_voting_ensemble(X, y, voting='hard'):
    voting_clf = VotingClassifier(
        voting=voting,
        estimators=[
            ('knn', KNeighborsClassifier()),
            ('dt', DecisionTreeClassifier()),
            ('lr', LogisticRegression(solver='sag', max_iter=10_000)),
            ('svc', SVC(probability=True)),
            ('mlp', MLPClassifier())
        ]
    )
    return voting_clf.fit(X, y)
#-----------------------------------------------------------------------------------------------------------------------
def task_4_bag_of_trees_ensemble(X, y):
##  n_estimators = 100
#   criterion = "gini", "entropy", or "log_loss"
##  max_depth = None, 1, 2, 3
#   min_samples_split = int, float
#   min_samples_leaf = int, float
#   min_weight_fraction_leaf = int, float
##  max_features = None, int, float, "sqrt", "log2"
#   max_leaf_nodes = int
#   min_impurity_decrease = float
#   bootstrap = True, False
#   ccp_alpha = non-negative float
#   max_samples = # only if bootstrap=True
    clf = RandomForestClassifier(n_estimators=84, max_depth=None, max_features='sqrt', random_state=42)
    clf.fit(X, y)
    return clf
#-----------------------------------------------------------------------------------------------------------------------
def create_stacked_data(voting_ensemble, X):
    stacked_list = []
    for estimator in voting_ensemble.estimators_:
        X_probs = estimator.predict_proba(X)
        stacked_list.append(X_probs)
    stacked_array = np.hstack(stacked_list)
    return stacked_array
#-----------------------------------------------------------------------------------------------------------------------
def task_6_stacked_ensemble(X_train, y_train, X_val, y_val):
    voting_ensemble = task_3_voting_ensemble(X_train, y_train, 'soft')
    stacked_data = create_stacked_data(voting_ensemble, X_val)
    blending_estimator = SVC(probability=True)
    blending_estimator.fit(stacked_data, y_val)
    return blending_estimator, voting_ensemble
#-----------------------------------------------------------------------------------------------------------------------
