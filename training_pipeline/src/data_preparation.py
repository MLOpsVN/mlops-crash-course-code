"""
Reference: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

Data preparation: The data is prepared for the ML task. This preparation involves data cleaning, where you split the data into training, validation, and test sets. You also apply data transformations and feature engineering to the model that solves the target task. The output of this step are the data splits in the prepared format.
"""

from utils import *

Log(AppConst.DATA_PREPARATION)


def prepare_data():
    Log().log.info("start prepare_data")
    Log().log.info("end prepare_data")


if __name__ == "__main__":
    prepare_data()
