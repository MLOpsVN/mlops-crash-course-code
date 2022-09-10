"""
Reference: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

Model evaluation: The model is evaluated on a holdout test set to evaluate the model quality. The output of this step is a set of metrics to assess the quality of the model.
"""

from utils import *

Log(AppConst.MODEL_EVALUATION)


def evaluate_model():
    Log().log.info("start evaluate_model")
    Log().log.info("end evaluate_model")


if __name__ == "__main__":
    evaluate_model()
