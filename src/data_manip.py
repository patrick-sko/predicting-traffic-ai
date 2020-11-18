import pandas as pd
import numpy as np
from sklearn.utils import shuffle

# random seed generated using https://www.random.org/ for shuffling dataset
# For reproducability
RANDOM_SEED = 187046186;

# Sampling configuration
TRAINING_PERCENT = 0.7;
TEST_PERCENT = 0.15;
VALIDATION_PERCENT = 0.15;


# Partition array by percentage
def partitionPercent(dataset, perc):
    splits = np.cumsum(perc)

    if splits[-1] != 1:
        raise ValueError("percents don't sum to 1")

    splits = splits[:-1]
    splits *= len(dataset)
    splits = splits.round().astype(np.int)

    return np.split(dataset, splits)


# Sample reproducibly according to defined proportions to training, test, and validation sets
def sample(dataset):

    # Shuffle data using random seed
    shuffledData = shuffle(dataset, random_state = RANDOM_SEED)
    # Partition based on constants
    partitionedData = partitionPercent(shuffledData, [TRAINING_PERCENT, TEST_PERCENT, VALIDATION_PERCENT])

    training = partitionedData[0];
    test = partitionedData[1];
    validation = partitionedData[2];

    return (training, validation, test)

# Specialized function to make TOD continuous
def numeric_tod(dataset):
    df = pd.DataFrame(dataset)
    # Expect TOd to have the format ##:##
    df.TOD = df.TOD.apply(lambda x : int(x[:2])*60+int(x[3:]))
    return df

def rush_hr_tod_dist(dataset):
    df = pd.DataFrame(dataset)
    # Expect TOd to have the format ##:##
    df["rush_dist"] = df.TOD.apply(lambda x : np.absolute(x - 800))
    return df

# Discretize data - partition a continuous feature into bins
# of equal frequency
def discretized_data(dataset, binsize, cont_ft):
    df = pd.DataFrame(dataset)
    for col in cont_ft:
        # partition using qcut for equally frequent bins
        df[col] = pd.qcut(dataset[col],10, labels=range(10))

    return df

