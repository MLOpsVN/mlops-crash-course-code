import pandas as pd

from utils import *

Log(AppConst.DATA_VALIDATION)
AppPath()


# Check data schema skews
def check_unexpected_features(df: pd.DataFrame):
    Log().log.info("start check_unexpected_features")
    config = Config()
    Log().log.info(f"config: {config.__dict__}")
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
    Log().log.info(f"config: {config.__dict__}")
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
