from feast import FeatureStore
import pandas as pd
from datetime import datetime

store = FeatureStore(repo_path="../feature_repo")

entity_df = pd.DataFrame.from_dict(
    {
        "driver_id": [1001, 1002, 1003, 1004, 1001],
        "event_timestamp": [
            datetime(2022, 4, 12, 10, 59, 42),
            datetime(2022, 4, 12, 8, 12, 10),
            datetime(2022, 4, 12, 16, 40, 26),
            datetime(2022, 4, 12, 15, 1, 12),
            datetime.now()
        ]
    }
)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_stats:acc_rate",
        "driver_stats:conv_rate"
    ],
).to_df()
print(training_df.head())