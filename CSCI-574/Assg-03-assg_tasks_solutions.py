import math
import numpy as np
import pandas as pd


def add_dummy_feature(x):
    """Add in a dummy column 0 of features.  All of the dummy feature values
    should be 1.0 for the newly added column feature.

    Arguments
    ---------
    x : numpy array of shape (n, m) with n samples and m features.
        The input data that needs a dummy feature added as column 0.

    Returns
    -------
    dummy_x : numpy now of shape (n, m+1) 
      Where a dummy column of 1.0 values has been added as column 0 to the
      original input array.
    """
    n, m = x.shape
    dummy_x = np.hstack([np.ones((n, 1)), x.copy()])
    return dummy_x


def predict(X, theta):
    """Compute the predictions for a set of data X given a set of model
    parameters theta.  The input data X is expected to have shape
    (n, m) of n input samples each with m features.  The theta model
    parameters should be a vector of shape (m,), matching the number of
    features of each input sample given.

    Arguments
    ---------
    X : numpy array of shape (n, m)
        Input data to compute predictions for.  This is an array of shape (n, m)
        with n samples in the input and each sample consists of m features, where it is
        assumed a dummy feature has already been added for this input.
    theta : numpy array of shape (m,)
        A set of model parameters, a vector of shape (m,).  The number of
        parameters in theta must macth the number of features in the input data
        X for this function to make predictions.

    Returns
    -------
    y_pred : numpy array of shape (n,)
       A vector with n predictions for each of the n samples given in the input data X
    """
    y_pred = X @ theta
    return y_pred


def loss_grad(X, theta, y_true):
    """Compute the loss of a model using the mean squared error MSE, as well as the
    gradients of the model with respect to the model parameters. This function returns
    the loss (a scalar value) and the gradients (a vector of shape (m,)).

    Arguments
    ---------
    X : numpy array of shape (n, m) 
        Input data to calculate loss and gradients with respect to los for.
    theta : numpy array of shape (m, )
        A set of model parameters, an vector of shape (m,).  The number of
        parameters in theta must mach the number of features in the input data
        X for this function to calculate loss and gradients.  This set of theta
        parameters are usually the current parameters during an optimized search
        being performed.
    y_true : numpy array of shape (n,)
        The true values that the model is trying to predict for this data.

    Returns
    -------
    loss : scalar
        A scalar value, the MSE loss of the given model for this data X
    gradients : numpy array of shape (m,)
        The gradients of the model with respect to each feature/theta parameter
    """
    n, m = X.shape

    # predictions of the current model
    y_pred = predict(X, theta)

    # errors, difference of predictions and true values
    # could reshape y_true to be column vector here, to ensure can handle
    # vectorized multi theta calculations
    errors = (y_pred - y_true)

    # mean squared error loss of this model
    # loss = (errors @ errors) / n
    loss = np.sum(errors**2.0, axis=0) / n

    # the gradients of this model with respect to the input features
    gradients = (X.T @ errors) * (2.0 / n)

    return loss, gradients


def gradient_descent(X, y_true, num_iter=50, eta=0.1):
    """Perform linear regression gradient descent optimization.  Given a set of data
    to fit in array X and the true label values in y_true, perform the indicated
    number of iterations of gradient descent.  This function starts with all theta
    optimization parameters at 0 and iterates from there.  

    Arguments
    ---------
    X : numpy array shape (n, m)
        Input data array to perform linear regression on using gradient descent.
    y_true : numpy array shape (n,)
        The vector of the true label values to perform linear regression model fit on.
    num_iter : scalar default 50
        The fixed number of gradient descent iterations to perform.
    eta : scalar default 0.1
        The learning rate, this is multiplied by the current gradients to determine the
        next gradient step to take along each model dimension.

    Returns
    -------
    theta : numpy array shape (m,)
        The fitted model parameters obtained after gradient descent optimization concludes
        on the data and labels being fitted.
    history : numpy array shape (num_iter,)
        An array of the loss values obtained during each iteration of gradient descent
        optimization.
    """
    # get the number of samples n and the number of features m
    n, m = X.shape

    # create initial parameters for gradient descent
    theta = np.zeros((m,))

    # will keep a list of losses obtained
    history = []

    for epoch in range(num_iter):
        # calculate current loss and gradients w/ respect to current theta model parameters
        loss, gradients = loss_grad(X, theta, y_true)

        # update history of losses over each epoch of the gradient descent
        history.append(loss)

        # follow gradients to update model parameters towards lower loss
        theta = theta - (eta * gradients)

    return theta, np.array(history)


def load_onefeature_dataset():
    """Load in the dataset and return only the first feature for use for most of the
    assignment.

    Returns
    -------
    x : numpy array shape (47,1)
        The one feature values for training/fitting regression models with.  Has a single column feature.
    y_true : numpy array shape (47,)
        The true labels for training/fitting regression on.  A vector of 47 real valued target labels.
    """
    # get the data from file
    data = np.genfromtxt('../data/data.csv', delimiter=',')

    # extract the features
    x = data[:, 0].reshape(-1, 1).copy()

    # get the true labels
    y_true = data[:, 4].copy()

    return x, y_true


def load_multifeature_dataset():
    """Load in the dataset, but this time return the full 4 features of the dataset for testing.

    Returns
    -------
    x : numpy array shape (47,4)
        The one feature values for training/fitting regression models with.  Has a single column feature.
    y_true : numpy array shape (47,)
        The true labels for training/fitting regression on.  A vector of 47 real valued target labels.
    """
    # get the data from file
    data = np.genfromtxt('../data/data.csv', delimiter=',')

    # extract the features
    x = data[:, :4].copy()

    # get the true labels
    y_true = data[:, 4].copy()

    return x, y_true
