"""
Reference: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

Data validation: This step is required before model training to decide whether you should retrain the model or stop the execution of the pipeline. This decision is automatically made if the following was identified by the pipeline.

Data schema skews: These skews are considered anomalies in the input data, which means that the downstream pipeline steps, including data processing and model training, receives data that doesn't comply with the expected schema. In this case, you should stop the pipeline so the data science team can investigate. The team might release a fix or an update to the pipeline to handle these changes in the schema. Schema skews include receiving unexpected features, not receiving all the expected features, or receiving features with unexpected values.

Data values skews: These skews are significant changes in the statistical properties of data, which means that data patterns are changing, and you need to trigger a retraining of the model to capture these changes.
"""

import pandas as pd

from utils import *

Log(AppConst.DATA_VALIDATION)
AppPath()


# Check data schema skews
def check_unexpected_features(df: pd.DataFrame):
    Log().log.info("start check_unexpected_features")
    config = Config()
    cols = set(df.columns)
    errors = []
    for col in cols:
        if not col in config.feature_dict:
            errors.append(f"feature {col} is not expected")

    if len(errors) > 0:
        raise Exception(errors)


def check_expected_features(df: pd.DataFrame):
    Log().log.info("start check_expected_features")
    config = Config()
    dtypes = dict(df.dtypes)
    errors = []
    for feature in config.feature_dict:
        if not feature in dtypes:
            errors.append(f"feature {feature} not found")
        else:
            expected_type = config.feature_dict[feature]
            real_type = dtypes[feature]
            if expected_type != real_type:
                errors.append(
                    f"feature {feature} expects type {expected_type}, received {real_type}"
                )

    if len(errors) > 0:
        raise Exception(errors)


# Check data values skews
def check_data_values_skews(df: pd.DataFrame):
    Log().log.info("start check_data_values_skews")


# combine
def validate_data():
    Log().log.info("start validate_data")
    inspect_curr_dir()

    df = load_df(AppPath.TRAINING_PQ)
    check_unexpected_features(df)
    check_expected_features(df)
    check_data_values_skews(df)


if __name__ == "__main__":
    validate_data()
