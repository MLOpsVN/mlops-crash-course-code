import pandas as pd

from bentoml import env, artifacts, api, BentoService
from bentoml.adapters import DataframeInput
from bentoml.frameworks.sklearn import SklearnModelArtifact

from prometheus_client import Summary

from feast import FeatureStore

REQUEST_TIME=Summary('request_processing_time', 'Time spend processing request')

store = FeatureStore(repo_path="../feature_repo")

@env(infer_pip_packages=True) # automatically infer necessary pip packages
@artifacts([SklearnModelArtifact('model')]) # since our model is scikit-learn based
class IrisClassifier(BentoService):
    # get online features from feature stores
    def retrieve_features(self, ids):
        features = store.get_online_features(
            features=[
                "driver_stats:acc_rate",
                "driver_stats:conv_rate"
            ],
            entity_rows=[
                {
                    "driver_id": ids,
                }
            ],
        ).to_dict(include_event_timestamps=True)
        return features
    
    @REQUEST_TIME.time()
    @api(input=DataframeInput(), batch=True)
    def predict(self, ids: pd.DataFrame):
        return self.artifacts.model.predict(ids)