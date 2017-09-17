
import keras.backend as T

def mean_absolute_deviation(y_true, y_pred):
    """"""
    return T.mean(T.abs(y_true - y_pred))

def sign_metric(y_true, y_pred):
    """Proportion with correct sign."""
    return T.mean(T.equal(T.sign(y_true), T.sign(y_pred)))

def constant_bid_expectation(y_true, y_pred):
    """With the strategy, "buy or short a constant quantity based on sign of prediction", the mean profit."""
    return T.mean(T.sign(y_pred)*y_true)

def smoothed_constant_bid_expectation(y_true, y_pred):
    """With the strategy, "buy or short a constant quantity based on sign of prediction", the expected profit. Smoothed near y_pred=0 for continuity"""
    epsilon = 0.1
    smooth_sign = T.tanh(y_pred/epsilon)*epsilon
    return T.mean(smooth_sign*y_true)

def smooth_mean_absolute_deviation(y_true, y_pred):
    """"""
    epsilon = .1
    smooth_abs = T.sqrt(T.square(y_pred - y_true)+epsilon)
    return T.mean(smooth_abs)