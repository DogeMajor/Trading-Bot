
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution1D
import timeseries_data
from keras_targets import sign_metric, constant_bid_expectation
from datetime import datetime

class SequentialModel:

    prediction_size = 30
    epochs = 40
    start = datetime(2010, 1, 1)

    def __init__(self, verbosity=0):

        self.verbosity = verbosity

        model = Sequential()
        model.add(Dense(10, activation='tanh', input_shape=(self.prediction_size,)))
        model.add(Dense(1, activation='tanh'))

        self.metrics = [sign_metric, constant_bid_expectation]
        model.compile(
            loss='mean_squared_error', 
            optimizer='adam', 
            metrics=self.metrics,
            )

        self.model = model

    def predict(self, ticker):

        # Observations = differences.
        # Missing data are interpolated, implying zero differences.
        closure_series = timeseries_data.closure_series(ticker, start=self.start)
        closure_diff = closure_series.interpolate().bfill().ffill().diff().iloc[1:]

        # Scale data to near unity
        data_scaler = StandardScaler()
        data_in_units = closure_diff.values
        data = data_scaler.fit_transform(data_in_units.reshape(-1, 1)).flatten()

        # Split data
        X_train, y_train, X_test, y_test, X_pred = training_and_test_split(data, self.prediction_size)

        #
        fit = self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=self.epochs, batch_size=30, verbose=self.verbosity)
        history = fit.history

        # Validate
        #validation_quantities = self.model.evaluate(X_test, y_test)
        #metric_names = [n if type(n)==str else n.__name__ for n in ['loss']+self.metrics]
        #validation_quantities = dict(zip(metric_names, validation_quantities))

        # To original units
        # WARNING: Duct tape
        quantities = {key[4:]: value[-1] for key, value in history.items() if key.startswith('val_')}
        quantities['constant_bid_expectation'] = data_scaler.inverse_transform([quantities['constant_bid_expectation']])[0]

        # Predict
        quantities['dimensionless_prediction'] = self.model.predict(X_pred)[0, 0]
        quantities['prediction'] = data_scaler.inverse_transform([quantities['dimensionless_prediction']])[0]

        return quantities


def vector_to_obs_arrays(data, size, N=None):
    """Split array into pairs of (input, output) represented as a matrix of shape (N, size) and vector (N,). 
    data           1D array of observations
    size            size of chunks
    N               number of chunks
    """
    # Figure out amount of observation pairs
    if N is None or N>len(data)-size-1:
        N = len(data)-size-1
    # Starting indices
    idx = np.random.choice(range(len(data)-size-1), N, replace=False)
    # Generate (vector, scalar) pairs 
    X, y = zip(*((data[i:i+size], data[i+size+1]) for i in idx))
    X, y = (np.asarray(a) for a in (X, y))
    # Make into appropriate arrays
    X_pred = data[-size:].reshape((1, -1))
    return X, y, X_pred

def training_and_test_split(data, prediction_size):
    """One third test data."""
    X, y, X_pred = vector_to_obs_arrays(data, prediction_size, None)
    y = y.reshape((-1, 1))
    train_cutoff = int(.6667*len(y))
    X_train, y_train = X[:train_cutoff], y[:train_cutoff]
    X_test, y_test = X[train_cutoff:], y[train_cutoff:]
    return X_train, y_train, X_test, y_test, X_pred

if __name__ == '__main__':
    model_container = SequentialModel()
    # prediction, metrics = model_container.predict('GOOG')
    predictions, metrics = zip(*(model_container.predict('AAPL') for _ in range(20)))
    
    from pylab import *
    ion()
    figure()
    hist(predictions)
    figure()
    hist([m['constant_bid_expectation'] for m in metrics])