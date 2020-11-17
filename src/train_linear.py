import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error

import linear_regression as lr
from data_manip import sample

# Path to save plots
PLOT_PATH = "../model/plots/"
# Path to processed data
DATA_PATH = "../data/processed/dataset-numeric-full.xlsx"

# Read Data set
dataset = pd.read_excel(DATA_PATH)

# Travel time is our response variable
RESPONSE_COL = "Travel Time"
# DATE which we do not take as explanatory
DATE_COL = "Date"
# All columns except Travel time and date are explanatory
EXPLANATORY_COLS = ["TOD","Day","Month","Holiday","Incidents","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]

(training, validation, test) =  sample(dataset)

individual_ft_regs = lr.train_regress_individual(training, EXPLANATORY_COLS, RESPONSE_COL)
individual_test_errors = lr.predict_regress_individual(individual_ft_regs, test, RESPONSE_COL)

for k,v in individual_test_errors.items():
    print("Testing Error of feature " + k + ": " + str(v))

# Plot a bar chart of individual error
plt.title("Mean squared errors of individual features")
plt.bar(range(len(individual_test_errors)), list(individual_test_errors.values()), align='center')
plt.xticks(range(len(individual_test_errors)), list(individual_test_errors.keys()))
plt.xlabel("feature")
plt.ylabel("mean squared error")
plt.savefig(PLOT_PATH + "regression_error_features_bar.png")

# An feature subset based on what intuitively affects the traffic
EXPLANATORY_SUBSET_INTUITION = ["TOD","Day","Month","Holiday","Incidents","temperature","weather_description","LaneClosures"]
reg_intuitive = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_INTUITION, RESPONSE_COL)
err_intuitive = lr.predict_regress_feature_set(reg_intuitive,training, EXPLANATORY_SUBSET_INTUITION , RESPONSE_COL)
print("intuitive features linear regression error:" + str(err_intuitive))

# An feature subset based on features that had low mean squared error
EXPLANATORY_SUBSET_LOW_ERROR = ["humidity", "wind_direction","wind_speed","LaneClosures"]
reg_low_error = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_LOW_ERROR , RESPONSE_COL)
err_low = lr.predict_regress_feature_set(reg_low_error, training, EXPLANATORY_SUBSET_LOW_ERROR, RESPONSE_COL)
print("low error features linear regression error:" + str(err_low))

# Testing on all features
reg_complete = lr.train_basic_regress_feature_set(training, EXPLANATORY_COLS, RESPONSE_COL)
err_complete = lr.predict_regress_feature_set(reg_complete, training, EXPLANATORY_COLS, RESPONSE_COL)
print("all features linear regression error:" + str(err_complete))


