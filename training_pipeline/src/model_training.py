"""
Reference: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

Model training: The data scientist implements different algorithms with the prepared data to train various ML models. In addition, you subject the implemented algorithms to hyperparameter tuning to get the best performing ML model. The output of this step is a trained model.
"""

from utils import *

Log(AppConst.MODEL_TRAINING)


def train_model():
    Log().log.info("start train_model")
    Log().log.info("end train_model")


if __name__ == "__main__":
    train_model()
