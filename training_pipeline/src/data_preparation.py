import pandas as pd
from sklearn.model_selection import train_test_split

from utils import *

Log(AppConst.DATA_PREPARATION)
AppPath()


def prepare_data(df: pd.DataFrame):
    Log().log.info("start prepare_data")
    inspect_curr_dir()

    config = Config()
    Log().log.info(f"config: {config.__dict__}")
    train, test = train_test_split(
        df, test_size=config.test_size, random_state=config.random_seed
    )
    target_col = config.target_col
    train_x = train.drop([target_col], axis=1)
    train_y = train[[target_col]]
    test_x = test.drop([target_col], axis=1)
    test_y = test[[target_col]]

    to_parquet(train_x, AppPath.TRAIN_X_PQ)
    to_parquet(train_y, AppPath.TRAIN_Y_PQ)
    to_parquet(test_x, AppPath.TEST_X_PQ)
    to_parquet(test_y, AppPath.TEST_Y_PQ)
    inspect_dir(AppPath.TRAIN_X_PQ.parent)


if __name__ == "__main__":
    df = load_df(AppPath.TRAINING_PQ)
    prepare_data(df)
