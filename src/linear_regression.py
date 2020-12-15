import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

from data_manip import sample

PLOT_PATH = "../model/linear_regression/plot/"

# Test individual features
# Returns a map of featurename:regressor
# If plot = True saves to plot
def train_regress_individual(trainingdata, explanatory_cols, response_col, plot=True):

    reg_map = {}

    Y = trainingdata[response_col].values.reshape(-1,1)

    for s in explanatory_cols:
        X = trainingdata[s].values.reshape(-1,1)
        reg = LinearRegression().fit(X,Y)
        reg_map[s] = reg

        if plot:
            plt.suptitle("Individual Linear Regression Feature - " + s)
            plt.scatter(X,Y)
            plt.plot(X, reg.predict(X),color="red")
            plt.xlabel(s)
            plt.ylabel("Travel time")
            plt.savefig(PLOT_PATH + "linear_regression_individual_ft_" + s + ".png")
            plt.clf()
    return reg_map 

# Predict individual features on test data using a map of regressors
# Meant to be composed with train_regress_individual
# returns map of column:(rmse_error, mae_error)
def predict_regress_individual(reg_map, testdata, response_col):
    # reg_map expected to be a map of column:regressor

    error_map = {}
    for s,reg in reg_map.items():
        test_feature_data = testdata[s].values.reshape(-1,1)
        test_predict = reg.predict(test_feature_data)

        rmse_error = np.sqrt(mean_squared_error(test_predict, testdata[response_col]))
        mae_error = mean_absolute_error(test_predict, testdata[response_col])
        error_map[s] = (rmse_error, mae_error)

    return error_map

# Train on set of features (expects multiple features)
def train_basic_regress_feature_set(trainingdata, explanatory_cols, response_col):
    X = trainingdata[explanatory_cols]
    Y = trainingdata[response_col]
    reg = LinearRegression().fit(X,Y)

    return reg

# predict a dataset returning the mean squared error and mean absolute error
def predict_regress_feature_set(reg, testdata, explanatory_cols, response_col):
    test_feature_data = testdata[explanatory_cols]
    test_predict = reg.predict(test_feature_data)

    rmse_error = np.sqrt(mean_squared_error(test_predict, testdata[response_col]))
    mae_error = mean_absolute_error(test_predict, testdata[response_col])
    return (rmse_error, mae_error)

# predict a dataset returning the predictions
def predict_regress(reg, testdata, explanatory_cols, response_col):
    test_feature_data = testdata[explanatory_cols]
    test_predict = reg.predict(test_feature_data)
    return test_predict

