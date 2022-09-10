"""
Reference: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

Data extraction: You select and integrate the relevant data from various data sources for the ML task.
"""

import feast
import pandas as pd

from utils import *

Log(AppConst.DATA_EXTRACTION)


def extract_data():
    Log().log.info("start extract_data")

    cwd = os.getcwd()
    Log().log.info(f"current dir: {cwd}")
    inspect_dir(cwd)

    inspect_dir(AppPath.FEATURE_STORE_ROOT)

    # Load driver order data
    orders = pd.read_csv(AppPath.DATA / "driver_orders.csv", sep="\t")
    orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])

    # Connect to your feature store provider
    fs = feast.FeatureStore(repo_path=AppPath.FEATURE_REPO)

    # Retrieve training data
    training_df = fs.get_historical_features(
        entity_df=orders,
        features=[
            "driver_stats:conv_rate",
            "driver_stats:acc_rate",
        ],
    ).to_df()

    Log().log.info("----- Feature schema -----")
    Log().log.info(training_df.info())

    Log().log.info("----- Example features -----")
    Log().log.info(training_df.head())

    Log().log.info("end extract_data")


if __name__ == "__main__":
    extract_data()
