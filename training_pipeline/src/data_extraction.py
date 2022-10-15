import feast
import pandas as pd

from utils import *

Log(AppConst.DATA_EXTRACTION)
AppPath()


def extract_data():
    Log().log.info("start extract_data")
    inspect_curr_dir()

    # Connect to your feature store provider
    inspect_dir(AppPath.DATA_SOURCES)
    inspect_dir(AppPath.FEATURE_REPO)
    fs = feast.FeatureStore(repo_path=AppPath.FEATURE_REPO)

    # Load driver order data
    inspect_dir(AppPath.DATA)
    orders = pd.read_csv(AppPath.DATA / "driver_orders.csv", sep="\t")
    orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])

    # Retrieve training data
    training_df = fs.get_historical_features(
        entity_df=orders,
        features=[
            "driver_stats:conv_rate",
            "driver_stats:acc_rate",
            "driver_stats:avg_daily_trips",
        ],
    ).to_df()

    training_df = training_df.drop(["event_timestamp", "driver_id"], axis=1)

    Log().log.info("----- Feature schema -----")
    Log().log.info(training_df.info())

    Log().log.info("----- Example features -----")
    Log().log.info(training_df.head())

    # Write to file
    to_parquet(training_df, AppPath.TRAINING_PQ)
    inspect_dir(AppPath.TRAINING_PQ.parent)


if __name__ == "__main__":
    extract_data()
