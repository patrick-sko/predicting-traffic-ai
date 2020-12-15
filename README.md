# predicting-traffic-ai
Project Description:
-------------------
The problem this project looks to solve is the ability to accurately predict the total travel time between two particular points on a Los Angeles Freeway, based on traffic sensor and weather. This project implements Multiple Linear Regression and Random Forest using the Python ```scikit-learn``` package, to predict the travel time. The models are trained on data from 2 separate data sets:
- Performance MeasurementSystem (PeMS): provides historical data collected by traffic sensors from freeways located in major metropolitan cities in California. This project constructs our regression models by looking at the 30.5 km route that begins in Long Beach Cal-ifornia and ends in downtown Los Angeles and follows the710-N freeway. (http://pems.dot.ca.gov/?s_time_id=1420416000&e_time_id=1420675140&route_id=85&html_x=40&report_form=1&dow_1=on&dnode=Route&content=tt&tab=tt_tod_time)
- Historical weather data set: provides historical weather data for 36 major cities across Canada, the United States, and Israel. This project uses the weather data for the city of Los Angeles to train our models. (https://www.kaggle.com/selfishgene/historical-hourly-weather-data?select=pressure.csv)

Data is taken from the 2 data sets for 2015, 2016, and 2017 and combined into one final data set with 207577 rows. This data set is available in predicting-traffic-ai/raw_data/dataset1.xlsx

Features:
---------
- Read in 200,000 rows of traffic and weather data
- Train a Simple Linear Regression model to determine the features that affect travel time the most
- Train a Multiple Linear Regression model with the features from the Simple Linear Regression Model to predict long term travel time
- Train a Random Forest model to repdict long term travel time
- Measure error in prediction accuracy with root mean square error(RMSE) and mean absolute error(MAE)
- Plot results of different experiments for the Simple Linear Regression, Multiple Linear Regression, and Random Forest models
- Plot heat maps to compare model predictions to actual travel time

Required Libraries:
-------------------
Pandas - for reading and manipulating data:
```
pip3 install pandas
```

Numpy - for sampling data and calculations:
```
pip3 install numpy
```

Scikit-learn - for training and testing our models:
```
pip3 install U scikit-learn
```

xlrd - for reading in data from XSLS file:
```
pip3 install xlrd
```

Matplotlib - for plotting results:
```
pip3 install matplotlib
```

Scipy Version 1.1.0 or higher - to satisfy a dependency between numpy and matplotlib:
```
pip3 install scipy==1.1.0
```
Running the Code:
-----------------
```
cd src/
```

Running linear regression training
```
python3 train_linear.py 
```

Running random forest training
```
python3 train_forest.py
```

Sample Ouput:
-------------
Outputs RMSE and MAE for every experiment run, example:

```
RMSE of Random forest on test data with 1100 trees generated, 1 features split on, and 50 max depth, using only predictable columns: 0.5509280279845497

MAE of Random forest on test data with 1100 trees generated, 1 features split on, and 50 max depth, using only predictable columns: 0.2981371357621692
```
