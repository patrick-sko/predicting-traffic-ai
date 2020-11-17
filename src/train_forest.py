import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from data_manip import discretized_data, sample

# Path to processed data
#DATA_PATH = "../data/processed/dataset1.xlsx"
DATA_PATH = "../data/processed/dataset-numeric-full.xlsx"

# Travel time is our response variable
RESPONSE_COL = "Travel Time"
# DATE which we do not take as explanatory
DATE_COL = "Date"
# All columns except Travel time and date are explanatory
EXPLANATORY_COLS = ["TOD","Day","Month","Holiday","Incidents","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]

# Which features are continuous
CONT_FT = ["TOD","humidity","pressure","temperature","wind_direction"]

# Read Data set
dataset = pd.read_excel(DATA_PATH)

# Discretize data set
discrete_data = (discretized_data(dataset, 10, CONT_FT))

# partition into training, test, and validation
(training, test, validation) =  sample(discrete_data)

X = training[EXPLANATORY_COLS]
Y = training[RESPONSE_COL]

reg = RandomForestRegressor().fit(X,Y)

test_predict = (reg.predict(test[EXPLANATORY_COLS]))
print("Error of Random forest on test data"\
        + ":" \
        + str(mean_squared_error(test_predict, test[RESPONSE_COL])))

#Get max depth in the forest
#print(max([estimator.get_depth() for estimator in reg.estimators_]))
