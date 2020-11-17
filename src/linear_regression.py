import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from data_manip import sample

MODEL_DIR = "../models/"

# Test individual features
# Returns a map of featurename:regressor
def train_regress_individual(trainingdata, explanatory_cols, response_col):

    reg_map = {}

    Y = trainingdata[response_col]

    for s in explanatory_cols:
        X = trainingdata[[s]].values.reshape(-1,1)
        reg = LinearRegression().fit(X,Y)
        reg_map[s] = reg

    return reg_map 

# Predict individual features on test data using a map of regressors
# Meant to be composed with train_regress_individual
def predict_regress_individual(reg_map, testdata, response_col):
    # reg_map expected to be a map of column:regressor

    error_map = {}
    for s,reg in reg_map.items():
        test_feature_data = testdata[s].values.reshape(-1,1)
        test_predict = reg.predict(test_feature_data)

        error = mean_squared_error(test_predict, testdata[response_col])
        error_map[s] = error

    return error_map

# Train on set of features (expects multiple features)
def train_basic_regress_feature_set(trainingdata, explanatory_cols, response_col):
    X = trainingdata[explanatory_cols]
    Y = trainingdata[response_col]
    reg = LinearRegression().fit(X,Y)

    return reg

# predict a dataset returning the mean squared error
def predict_regress_feature_set(reg, testdata, explanatory_cols, response_col):
    test_feature_data = testdata[explanatory_cols]
    test_predict = reg.predict(test_feature_data)

    error = mean_squared_error(test_predict, testdata[response_col])
    return error
