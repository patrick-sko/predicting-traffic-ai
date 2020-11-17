import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import linear_regression as lr
from data_manip import sample

# Path to save plots
COMPARISON_PLOT_PATH = "../model/linear_regression/comparison/"
# Path to processed data
DATA_PATH = "../data/processed/dataset-numeric-full.xlsx"

# Read Data set
dataset = pd.read_excel(DATA_PATH)

# Travel time is our response variable
RESPONSE_COL = "Travel Time"
# DATE which we do not take as explanatory
DATE_COL = "Date"
# All columns except Travel time and date are explanatory
EXPLANATORY_COLS = ["Date", "TOD","Day","Month","Holiday","Incidents","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]

(training, validation, validation) =  sample(dataset)

individual_ft_regs = lr.train_regress_individual(training, EXPLANATORY_COLS, RESPONSE_COL)
individual_validation_errors = lr.predict_regress_individual(individual_ft_regs, validation, RESPONSE_COL)

print("Individual feature Errors:")
for k,(v1,v2) in individual_validation_errors.items():
    print("validation RMSE of feature " + k + ": " + str(v1))

for k,(v1,v2) in individual_validation_errors.items():
    print("validation MAE of feature " + k + ": " + str(v2))
    individual_validation_errors[k] = v1

# Plot a bar chart of individual error
plt.suptitle("Mean squared errors of individual features")
plt.figure(figsize = (22,10))
plt.bar(range(len(individual_validation_errors)), list(individual_validation_errors.values()), align='center')
plt.xticks(range(len(individual_validation_errors)), list(individual_validation_errors.keys()), fontsize=10, wrap=True)
plt.xlabel("feature")
plt.ylabel("root mean squared error")
plt.savefig(COMPARISON_PLOT_PATH + "linear_regression_individual_bar.png")

print("==================================================================")
print("Feature subset Error:")
subset_validation_errors = {}
# An feature subset based on what intuitively affects the traffic
EXPLANATORY_SUBSET_INTUITION = ["Date", "TOD","Day","Month","Holiday","Incidents","temperature","weather_description","LaneClosures"]
reg_intuitive = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_INTUITION, RESPONSE_COL)
err_intuitive = lr.predict_regress_feature_set(reg_intuitive,training, EXPLANATORY_SUBSET_INTUITION , RESPONSE_COL)
subset_validation_errors["inuitivive"] = err_intuitive

# An feature subset based on features that had low mean squared error
EXPLANATORY_SUBSET_LOW_ERROR_FEW = ["Date", "humidity", "wind_direction","wind_speed","LaneClosures"]
reg_low_error_few = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_LOW_ERROR_FEW , RESPONSE_COL)
err_low_few = lr.predict_regress_feature_set(reg_low_error_few, training, EXPLANATORY_SUBSET_LOW_ERROR_FEW, RESPONSE_COL)
subset_validation_errors["lowest error"] = err_low_few

# Forecastable features (that can be predicted)
EXPLANATORY_SUBSET_PREDICTABLE = ["Date", "TOD","Day","Month","Holiday","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]
reg_predictable = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
err_predictable = lr.predict_regress_feature_set(reg_predictable, training, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
subset_validation_errors["forecastable features"] = err_predictable

# Date only features
EXPLANATORY_SUBSET_DATE_ONLY = ["Date", "TOD","Day","Month","Holiday"]
reg_date = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
err_date = lr.predict_regress_feature_set(reg_date, training, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
subset_validation_errors["date only"] = err_date

# Training on all features
reg_complete = lr.train_basic_regress_feature_set(training, EXPLANATORY_COLS, RESPONSE_COL)
err_complete = lr.predict_regress_feature_set(reg_complete, training, EXPLANATORY_COLS, RESPONSE_COL)
subset_validation_errors["full"] = err_complete

for k,(v1,v2) in subset_validation_errors.items():
    print("validation RMSE of " + k + "feature subset: " + str(v1))

for k,(v1,v2) in subset_validation_errors.items():
    print("validation MAE of " + k + "feature subset: " + str(v1))
    subset_validation_errors[k] = v1

# plot feature subset errors in bar graph
plt.suptitle("Root Mean squared errors of feature subsets")
plt.figure(figsize = (12,5))
plt.bar(range(len(subset_validation_errors)), list(subset_validation_errors.values()), align='center')
plt.xticks(range(len(subset_validation_errors)), list(subset_validation_errors.keys()), fontsize=10)
plt.xlabel("feature subset")
plt.ylabel("root mean squared error")
plt.savefig(COMPARISON_PLOT_PATH + "linear_regression_subset_bar.png")
