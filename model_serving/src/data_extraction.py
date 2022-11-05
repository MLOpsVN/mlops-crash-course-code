import feast
import pandas as pd

from utils import *

Log(AppConst.DATA_EXTRACTION)
AppPath()


def extract_data():
    Log().log.info("start extract_data")
    inspect_curr_dir()
    config = Config()
    Log().log.info(f"config: {config.__dict__}")

    # Connect to your feature store provider
    inspect_dir(AppPath.DATA_SOURCES)
    inspect_dir(AppPath.FEATURE_REPO)
    fs = feast.FeatureStore(repo_path=AppPath.FEATURE_REPO)

    # Load driver order data
    batch_input_file = AppPath.ROOT / config.batch_input_file
    inspect_dir(batch_input_file)
    orders = pd.read_csv(batch_input_file, sep="\t")
    orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])

    # Retrieve training data
    batch_input_df = fs.get_historical_features(
        entity_df=orders,
        features=[
            "driver_stats:conv_rate",
            "driver_stats:acc_rate",
            "driver_stats:avg_daily_trips",
        ],
    ).to_df()

    batch_input_df = batch_input_df.drop(["event_timestamp", "driver_id"], axis=1)

    Log().log.info("----- Feature schema -----")
    Log().log.info(batch_input_df.info())

    Log().log.info("----- Example features -----")
    Log().log.info(batch_input_df.head())

    # Write to file
    to_parquet(batch_input_df, AppPath.BATCH_INPUT_PQ)
    inspect_dir(AppPath.BATCH_INPUT_PQ)


if __name__ == "__main__":
    extract_data()
