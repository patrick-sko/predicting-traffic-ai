import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from data_manip import discretized_data, sample

# Path to processed data
#DATA_PATH = "../data/processed/dataset1.xlsx"
DATA_PATH = "../data/processed/dataset-numeric-full.xlsx"

# Path to folder for figures
PLOT_PATH = "../model/random_forest/"

# Travel time is our response variable
RESPONSE_COL = "Travel Time"
# DATE which we do not take as explanatory
DATE_COL = "Date"

TOD_COL = "TOD"
# All columns except Travel time and date are explanatory
EXPLANATORY_COLS = ["Date","TOD","Day","Month","Holiday","Incidents","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]

# Only columns that can be predicted -- excluding: incidents
PREDICTABLE_COLS = ["Date","TOD","Day","Month","Holiday","humidity","pressure","temperature","weather_description","wind_direction","wind_speed","LaneClosures"]

# Which features are continuous
CONT_FT = ["TOD","humidity","pressure","temperature","wind_direction"]

# Read Data set
dataset = pd.read_excel(DATA_PATH)

# Discretize data set
discrete_data = (discretized_data(dataset, 10, CONT_FT))

# partition into training, test, and validation
(training, validation, test) =  sample(discrete_data)


X = training[EXPLANATORY_COLS]
Y = training[RESPONSE_COL]

XPredictable = training[PREDICTABLE_COLS]

# nValuesSmall = np.arange(10, 100, 10)
# nValues = np.arange(100, 1200, 200)
nAll = []
nVal = 10
while nVal < 100:
        nAll.append(nVal)
        nVal+=10
while nVal < 1200:
        nAll.append(nVal)
        nVal+=200

# nAll = np.concatenate((nValuesSmall, nValues))
mValues = []
mVal = 1
while mVal < 14:
        mValues.append(mVal)
        mVal+=1

# mValues = np.arange(1, 14)
dValues = []
dVal = 10 
while dVal < 52:
        dValues.append(dVal)
        dVal+=2

# dValues = np.arange(10, 50, 2)
# nMSE = nAll
# mMSE = np.arange(1, 13)
# dMSE = np.arange(10, 50, 2)

nMSE = []
nMAE = []
mMSE = []
mMAE = []
dMSE = []
dMAE = []

minNSmallError = 100
minErrorN = 100
minErrorM = 100
minErrorD = 100
optimalSmallN = 0
optimalN = 1100
optimalM = 1
optimalD = 0

#setting random_state=seed for all RF below to produce deterministic results

# Finding optimal number of trees for RF
print("==================================================================")
print("n_estimator Error:")
for n in nAll:
        regN = RandomForestRegressor(n_estimators=n, random_state=0).fit(X,Y)

        val_predict = (regN.predict(validation[EXPLANATORY_COLS]))
        errorN = np.sqrt(mean_squared_error(val_predict, validation[RESPONSE_COL]))
        errorNMAE = mean_absolute_error(val_predict, validation[RESPONSE_COL])
        nMSE.append(errorN)
        nMAE.append(errorNMAE)
        # i+=1
        if (errorN < minErrorN): 
                optimalN = n
        print("RMSE of Random forest on test data with {} trees generated: {}".format(n, errorN))
        print("MAE of Random forest on test data with {} trees generated: {}".format(n, errorNMAE))


figN, axN = plt.subplots()
axN.plot(nAll, nMSE, label="RMSE")
axN.plot(nAll, nMAE, label="MAE")
axN.set_xlabel("n_estimators in RandomForestRegressor")
axN.set_ylabel("Error")
axN.set_title("RMSE and MAE variation in Random Forest with \n different n_estimators")
axN.legend()
figN.savefig(PLOT_PATH + "RF-n-estimators.png")

# Finding optimal number of values to split on
print("==================================================================")
print("max_features Error:")
for m in mValues:
        regM = RandomForestRegressor(max_features=m, random_state=0).fit(X,Y)

        val_predict = (regM.predict(validation[EXPLANATORY_COLS]))
        errorM = np.sqrt(mean_squared_error(val_predict, validation[RESPONSE_COL]))
        errorMMAE = mean_absolute_error(val_predict, validation[RESPONSE_COL])
        mMSE.append(errorM)
        mMAE.append(errorMMAE)
        # j+=1
        if (errorM < minErrorM): 
                optimalM = m

        print("RSME of Random forest on test data with {} features split on: {}".format(m, errorM))
        print("MAE of Random forest on test data with {} features split on: {}".format(m, errorMMAE))


figM, axM = plt.subplots()
axM.plot(mValues, mMSE, label="RMSE")
axM.plot(mValues, mMAE, label="MAE")
axM.set_xlabel("max_features in RandomForestRegressor")
axM.set_ylabel("Error")
axM.set_title("RMSE and MAE variation in RandomForestRegressor with \n different max_features")
axM.legend()
figM.savefig(PLOT_PATH + "RF-max-features.png")

# Finding optimal max depth
print("==================================================================")
print("max_depth Error:")
for d in dValues:
        regD = RandomForestRegressor(max_depth=d, random_state=0).fit(X,Y)
        val_predict = (regD.predict(validation[EXPLANATORY_COLS]))
        errorD = np.sqrt(mean_squared_error(val_predict, validation[RESPONSE_COL]))
        errorDMAE = mean_absolute_error(val_predict, validation[RESPONSE_COL])
        dMSE.append(errorD)
        dMAE.append(errorDMAE)
        # k+=1
        if (errorD < minErrorD): 
                optimalD = d
        print("RMSE of Random forest on test data with a max depth of {}: {}".format(d, errorD))
        print("MAE of Random forest on test data with a max depth of {}: {}".format(d, errorDMAE))

figD, axD = plt.subplots()
axD.plot(dValues, dMSE, label="RMSE")
axD.plot(dValues, dMAE, label="MAE")
axD.set_xlabel("max_depth in RandomForestRegressor")
axD.set_ylabel("Error")
axD.set_title("RMSE and MAE variation in RandomForestRegressor \n with different max_depth")
axD.legend()
figD.savefig(PLOT_PATH + "RF-max-depth.png")

print("==================================================================")
print("Random Forest Model (No Tuning) Errors:")
# Final regression with non optimal values
regNonOptimal = RandomForestRegressor(random_state=0).fit(X,Y)
test_predict = (regNonOptimal.predict(test[EXPLANATORY_COLS]))
errorNonOptimnal = np.sqrt(mean_squared_error(test_predict, test[RESPONSE_COL]))
errorNonOptimnalMAE = mean_absolute_error(test_predict, test[RESPONSE_COL])
print("RMSE of Random forest on test data with default values for n_estimators (100), max_features(13), and max_deppth(none): {}".format(errorNonOptimnal))
print("MAE of Random forest on test data with default values for n_estimators (100), max_features(13), and max_deppth(none): {}".format(errorNonOptimnalMAE))

# Final regression with optimal values
print("==================================================================")
print("Random Forest Model (Optimal Values) Errors:")
regFinal = RandomForestRegressor(n_estimators=optimalN, max_features=optimalM, max_depth=optimalD, random_state=0).fit(X,Y)
test_predict = (regFinal.predict(test[EXPLANATORY_COLS]))
errorFinal = np.sqrt(mean_squared_error(test_predict, test[RESPONSE_COL]))
errorFinalMAE = mean_absolute_error(test_predict, test[RESPONSE_COL])
print("RMSE of Random forest on test data with {} trees generated, {} features split on, and {} max depth: {}".format(optimalN, optimalM, optimalD, errorFinal))
print("MAE of Random forest on test data with {} trees generated, {} features split on, and {} max depth: {}".format(optimalN, optimalM, optimalD, errorFinalMAE))

# Final regression with optimal values and only predictable columns
print("==================================================================")
print("Random Forest Model (Predictable Columns and Optimal Values) Errors:")
regFinalPredictable = RandomForestRegressor(n_estimators=optimalN, max_features=optimalM, max_depth=optimalD, random_state=0).fit(XPredictable,Y)
test_predict = (regFinalPredictable.predict(test[PREDICTABLE_COLS]))
errorPredictable = np.sqrt(mean_squared_error(test_predict, test[RESPONSE_COL]))
errorPredictableMAE = mean_absolute_error(test_predict, test[RESPONSE_COL])

print("RMSE of Random forest on test data with {} trees generated, {} features split on, and {} max depth, using only predictable columns: {}".format(optimalN, optimalM, optimalD, errorPredictable))
print("MAE of Random forest on test data with {} trees generated, {} features split on, and {} max depth, using only predictable columns: {}".format(optimalN, optimalM, optimalD, errorPredictableMAE))

dataset = pd.read_excel(DATA_PATH)
CONT_FT_RAW = ["humidity","pressure","temperature","wind_direction"]
rawData = (discretized_data(dataset, 10, CONT_FT_RAW))
(trainingRaw, validationRaw, testRaw) =  sample(rawData)

closeTest = 0.003*test[RESPONSE_COL]
closePredict = 0.003*test_predict
closeTestOverlay = [[0, 0, 1]]
closePredictOverlay = [[1, 0, 0]]

figH, axH = plt.subplots()
axH.scatter(testRaw[TOD_COL], test[RESPONSE_COL], c=closeTest,  alpha=0.5)
axH.set_xlabel("TOD")
axH.set_ylabel("Travel Time")
axH.set_title("Actual Travel time")
figH.savefig("heatMapActual.png")

figP, axP = plt.subplots()
axP.scatter(testRaw[TOD_COL], test_predict, c=closePredict, alpha=0.5)
axP.set_xlabel("TOD")
axP.set_ylabel("Travel Time")
axP.set_title("Randolm Forest Predicted Travel time")
figP.savefig("heatMapPredictForest.png")

figC, axC = plt.subplots()
axC.scatter(testRaw[TOD_COL], test[RESPONSE_COL], c=closeTestOverlay, alpha=0.5, label="Actual Travel Time")
axC.scatter(testRaw[TOD_COL], test_predict, c=closePredictOverlay, alpha=0.5, label="Predicted Travel Time")
axC.set_xlabel("TOD")
axC.set_ylabel("Travel Time")
axC.set_title("Predicted Travel time")
axC.legend()
figC.savefig("heatMapCombined.png")
