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

nValuesSmall = np.arange(10, 100, 10)
nValues = np.arange(100, 1100, 200)
nAll = np.concatenate((nValuesSmall, nValues))
mValues = np.arange(1, 13)
dValues = np.arange(10, 50, 2)
nMSE = nAll
dMSE = np.arange(1, 13)
mMSE = np.arange(10, 50, 2)
minNSmallError = 100
minErrorN = 100
minErrorM = 100
minErrorD = 100
optimalSmallN = 0
optimalN = 0
optimalM = 0
optimalD = 0

#setting random_state=seed for all RF below to produce deterministic results

# Finding optimal number of trees for RF

i = 0
for n in nAll:
        regN = RandomForestRegressor(n_estimators=n, random_state=0).fit(X,Y)

        val_predict = (regN.predict(validation[EXPLANATORY_COLS]))
        errorN = mean_squared_error(val_predict, validation[RESPONSE_COL])
        nMSE[i] = errorN
        i+=1
        if (errorN < minErrorN): 
                optimalN = n
        print("Error of Random forest on test data with "\
                + str(n) + " trees generated" \
                + ": " \
                + str(errorN))


figN, axN = plt.subplots()
axN.plot(nAll, nMSE, label="Validation Set")
axN.set_xlabel("n_estimators in RandomForestRegressor")
axN.set_ylabel("MSE")
axN.set_title("MSE variation in RandomForestRegressor with different n_estimators")
axN.legend()
figN.savefig("MSE-RF-n-estimators.png")

# if (minNSmallError < 1.4954692245966177):
#         n = optimalSmallN
# else:
#         n = 1.4954692245966177

# Finding optimal number of values to split on

j = 0
for m in mValues:
        regM = RandomForestRegressor(max_features=m, random_state=0).fit(X,Y)

        val_predict = (regM.predict(validation[EXPLANATORY_COLS]))
        errorM = mean_squared_error(val_predict, validation[RESPONSE_COL])
        nMSE[j] = errorM
        j+=1
        if (errorM < minErrorM): 
                optimalM = m

        print("Error of Random forest on test data with "\
                + str(m) + " features split on" \
                + ": " \
                + str(errorM))

figM, axM = plt.subplots()
axM.plot(mValues, mMSE, label="Validation Set")
axM.set_xlabel("max_features in RandomForestRegressor")
axM.set_ylabel("MSE")
axM.set_title("MSE variation in RandomForestRegressor with different max_features")
axM.legend()
figM.savefig("MSE-RF-max-features.png")

# Finding optimal max depth
k = 0
for d in dValues:
        regD = RandomForestRegressor(max_depth=d, random_state=0).fit(X,Y)
        val_predict = (regD.predict(validation[EXPLANATORY_COLS]))
        errorD = mean_squared_error(val_predict, validation[RESPONSE_COL])
        nMSE[k] = errorD
        k+=1
        if (errorD < minErrorD): 
                optimalD = d
        print("Error of Random forest on test data with a max depth of "\
                + str(optimalD) \
                + " : " \
                + str(errorD)) 

figD, axD = plt.subplots()
axD.plot(dValues, dMSE, label="Validation Set")
axD.set_xlabel("max_depth in RandomForestRegressor")
axD.set_ylabel("MSE")
axD.set_title("MSE variation in RandomForestRegressor with different max_depth")
axD.legend()
figD.savefig("MSE-RF-max-depth.png")

# Final regression with optimal values
regFinal = RandomForestRegressor(n_estimators=optimalN, max_features=optimalM, max_depth=optimalD, random_state=0).fit(X,Y)
test_predict = (regFinal.predict(test[EXPLANATORY_COLS]))
errorFinal = mean_squared_error(test_predict, test[RESPONSE_COL])
print("Error of Random forest on test data with "\
        + str(optimalN) + "trees generated and " + str(optimalM) + "features split on" \
        + " : " \
        + str(errorFinal)) 


# Final regression with optimal values and only predictable columns
regFinalPredictable = RandomForestRegressor(n_estimators=optimalN, max_features=optimalM, max_depth=optimalD, random_state=0).fit(XPredictable,Y)
test_predict = (regFinalPredictable.predict(test[PREDICTABLE_COLS]))
errorPredictable = mean_squared_error(test_predict, test[RESPONSE_COL])
print("Error of Random forest on test data with "\
        + str(optimalN) + "trees generated and " + str(optimalM) + "features split on, using only predictable columns" \
        + " : " \
        + str(errorPredictable)) 
