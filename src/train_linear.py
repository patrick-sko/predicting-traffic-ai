import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import linear_regression as lr
from data_manip import rush_hr_tod_dist,sample

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

(training, validation, test) =  sample(dataset)

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
plt.clf()

print("==================================================================")
print("Feature subset Error:")
subset_validation_errors = {}
# An feature subset based on what intuitively affects the traffic
EXPLANATORY_SUBSET_INTUITION = ["Date", "TOD","Day","Month","Holiday","Incidents","temperature","weather_description","LaneClosures"]
reg_intuitive = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_INTUITION, RESPONSE_COL)
err_intuitive = lr.predict_regress_feature_set(reg_intuitive,validation, EXPLANATORY_SUBSET_INTUITION , RESPONSE_COL)
subset_validation_errors["inuitivive"] = err_intuitive

# An feature subset based on features that had low mean squared error
EXPLANATORY_SUBSET_LOW_ERROR_FEW = ["Date", "humidity", "wind_direction","wind_speed","LaneClosures"]
reg_low_error_few = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_LOW_ERROR_FEW , RESPONSE_COL)
err_low_few = lr.predict_regress_feature_set(reg_low_error_few, validation, EXPLANATORY_SUBSET_LOW_ERROR_FEW, RESPONSE_COL)
subset_validation_errors["lowest error"] = err_low_few

# Forecastable features (that can be predicted)
EXPLANATORY_SUBSET_PREDICTABLE = ["Date", "TOD","Day","Month","Holiday","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]
reg_predictable = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
err_predictable = lr.predict_regress_feature_set(reg_predictable, validation, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
subset_validation_errors["forecastable features"] = err_predictable

# Date only features
EXPLANATORY_SUBSET_DATE_ONLY = ["Date", "TOD","Day","Month","Holiday"]
reg_date = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
err_date = lr.predict_regress_feature_set(reg_date, validation, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
subset_validation_errors["date only"] = err_date

# Training on all features
reg_complete = lr.train_basic_regress_feature_set(training, EXPLANATORY_COLS, RESPONSE_COL)
err_complete = lr.predict_regress_feature_set(reg_complete, validation, EXPLANATORY_COLS, RESPONSE_COL)
subset_validation_errors["full"] = err_complete

rmse_errors = {} 
mae_errors = {} 
for k,(v1,v2) in subset_validation_errors.items():
    print("validation RMSE of " + k + " feature subset: " + str(v1))
    rmse_errors[k] = v1

for k,(v1,v2) in subset_validation_errors.items():
    print("validation MAE of " + k + " feature subset: " + str(v2))
    mae_errors[k] = v2

# plot feature subset errors in bar graph
plt.suptitle("Root Mean squared errors of feature subsets")
plt.figure(figsize = (12,5))
plt.bar(range(len(rmse_errors)), list(rmse_errors.values()), align='center')
plt.xticks(range(len(rmse_errors)), list(rmse_errors.keys()), fontsize=10)
plt.xlabel("feature subset")
plt.ylabel("root mean squared error")
plt.savefig(COMPARISON_PLOT_PATH + "linear_regression_RMSE_subset_bar.png")
plt.clf()

# plot feature subset errors in bar graph
plt.suptitle("Root Mean absolute errors of feature subsets")
plt.figure(figsize = (12,5))
plt.bar(range(len(mae_errors)), list(mae_errors.values()), align='center')
plt.xticks(range(len(mae_errors)), list(mae_errors.keys()), fontsize=10)
plt.xlabel("feature subset")
plt.ylabel("root mean squared error")
plt.savefig(COMPARISON_PLOT_PATH + "linear_regression_MAE_subset_bar.png")
plt.clf()
dataset_rush_hr = rush_hr_tod_dist(dataset)
(training_tune,validation_tune, test_tune) =  sample(dataset)

print("==================================================================")
print("Tuned Error:")

#Tuned rush hour distance
RUSH_DIST = ["rush_dist"]
train_individ_tune = lr.train_regress_individual(training_tune, RUSH_DIST, RESPONSE_COL)
predict_individ_tune = lr.predict_regress_individual(train_individ_tune, training_tune, RESPONSE_COL)

for k,(v1,v2) in predict_individ_tune.items():
    print("validation RMSE of feature " + k + ": " + str(v1))
    print("validation MAE of feature " + k + ": " + str(v2))

EXPLANATORY_SUBSET_INTUITION = ["Date", "rush_dist","Day","Month","Holiday","Incidents","temperature","weather_description","LaneClosures"]
reg_intuitive = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_SUBSET_INTUITION, RESPONSE_COL)
err_intuitive = lr.predict_regress_feature_set(reg_intuitive,validation_tune, EXPLANATORY_SUBSET_INTUITION , RESPONSE_COL)
subset_validation_errors["inuitivive"] = err_intuitive

# Forecastable features (that can be predicted)
EXPLANATORY_SUBSET_PREDICTABLE = ["Date", "rush_dist","Day","Month","Holiday","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]
reg_predictable = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
err_predictable = lr.predict_regress_feature_set(reg_predictable, validation_tune, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
subset_validation_errors["forecastable features"] = err_predictable

# Date only features
EXPLANATORY_SUBSET_DATE_ONLY = ["Date", "rush_dist","Day","Month","Holiday"]
reg_date = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
err_date = lr.predict_regress_feature_set(reg_date, validation_tune, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
subset_validation_errors["date only"] = err_date

# training_tune on all features
EXPLANATORY_COLS_TUNED = ["Date", "rush_dist","Day","Month","Holiday","Incidents","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]
reg_complete = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_COLS_TUNED, RESPONSE_COL)
err_complete = lr.predict_regress_feature_set(reg_complete, validation_tune, EXPLANATORY_COLS_TUNED, RESPONSE_COL)
subset_validation_errors["full"] = err_complete

for k,(v1,v2) in subset_validation_errors.items():
    print("validation RMSE of " + k + " feature subset for tuned data: " + str(v1))
    rmse_errors[k] = v1

for k,(v1,v2) in subset_validation_errors.items():
    print("validation MAE of " + k + " feature subset for tuned data: " + str(v2))
    mae_errors[k] = v2

print("==============================================")
print("Test tuned prediction")
subset_test_errors = {}
EXPLANATORY_SUBSET_INTUITION = ["Date", "rush_dist","Day","Month","Holiday","Incidents","temperature","weather_description","LaneClosures"]
reg_intuitive = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_SUBSET_INTUITION, RESPONSE_COL)
err_intuitive = lr.predict_regress_feature_set(reg_intuitive,test_tune, EXPLANATORY_SUBSET_INTUITION , RESPONSE_COL)
subset_test_errors["inuitivive"] = err_intuitive

# Forecastable features (that can be predicted)
EXPLANATORY_SUBSET_PREDICTABLE = ["Date", "rush_dist","Day","Month","Holiday","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]
reg_predictable = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
err_predictable = lr.predict_regress_feature_set(reg_predictable, test_tune, EXPLANATORY_SUBSET_PREDICTABLE, RESPONSE_COL)
subset_test_errors["forecastable features"] = err_predictable

# An feature subset based on features that had low mean squared error
EXPLANATORY_SUBSET_LOW_ERROR_FEW = ["Date", "humidity", "wind_direction","wind_speed","LaneClosures"]
reg_low_error_few = lr.train_basic_regress_feature_set(training, EXPLANATORY_SUBSET_LOW_ERROR_FEW , RESPONSE_COL)
err_low_few = lr.predict_regress_feature_set(reg_low_error_few, test_tune, EXPLANATORY_SUBSET_LOW_ERROR_FEW, RESPONSE_COL)
subset_test_errors["lowest error"] = err_low_few

# Date only features
EXPLANATORY_SUBSET_DATE_ONLY = ["Date", "rush_dist","Day","Month","Holiday"]
reg_date = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
err_date = lr.predict_regress_feature_set(reg_date, test_tune, EXPLANATORY_SUBSET_DATE_ONLY, RESPONSE_COL)
subset_test_errors["date only"] = err_date

# training_tune on all features
EXPLANATORY_COLS_TUNED = ["Date", "rush_dist","Day","Month","Holiday","Incidents","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]
reg_complete = lr.train_basic_regress_feature_set(training_tune, EXPLANATORY_COLS_TUNED, RESPONSE_COL)
err_complete = lr.predict_regress_feature_set(reg_complete, test_tune, EXPLANATORY_COLS_TUNED, RESPONSE_COL)
subset_test_errors["full"] = err_complete


for k,(v1,v2) in subset_test_errors.items():
    print("test RMSE of " + k + " feature subset for tuned data: " + str(v1))
    rmse_errors[k] = v1

for k,(v1,v2) in subset_test_errors.items():
    print("test MAE of " + k + " feature subset for tuned data: " + str(v2))
    mae_errors[k] = v2
