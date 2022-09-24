from typing import Any, Dict, List, Optional

import bentoml
import feast
import mlflow
import numpy as np
from bentoml.io import JSON, NumpyNdarray
from mlflow.models.signature import ModelSignature
from pydantic import BaseModel

from utils import *

Log(AppConst.BENTOML_SERVICE)
AppPath()


def save_model() -> bentoml.Model:
    Log().log.info("start save_model")
    # read from .env file registered_model_version.json, get model name, model version
    config = Config()

    registered_model_file = AppPath.ROOT / config.registered_model_file
    Log().log.info(f"registered_model_file: {registered_model_file}")
    registered_model_dict = load_json(registered_model_file)

    run_id = registered_model_dict["_run_id"]
    model_name = registered_model_dict["_name"]
    model_version = registered_model_dict["_version"]
    model_uri = registered_model_dict["_source"]

    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    mlflow_model = mlflow.pyfunc.load_model(model_uri=model_uri)
    Log().log.info(mlflow_model.__dict__)
    model = mlflow_model._model_impl
    model_signature: ModelSignature = mlflow_model.metadata.signature

    # construct feature list
    feature_list = []
    for name in model_signature.inputs.input_names():
        feature_list.append(name)

    # save model using bentoml
    bentoml_model = bentoml.sklearn.save_model(
        model_name,
        model,
        # model signatures for runner inference
        signatures={
            "predict": {
                "batchable": False,
            },
        },
        labels={
            "owner": "mlopsvn",
        },
        metadata={
            "mlflow_run_id": run_id,
            "mlflow_model_name": model_name,
            "mlflow_model_version": model_version,
        },
        custom_objects={
            "feature_list": feature_list,
        },
    )
    Log().log.info(bentoml_model)
    return bentoml_model


bentoml_model = save_model()
feature_list = bentoml_model.custom_objects["feature_list"]
bentoml_runner = bentoml.sklearn.get(bentoml_model.tag).to_runner()
svc = bentoml.Service(bentoml_model.tag.name, runners=[bentoml_runner])
fs = feast.FeatureStore(repo_path=AppPath.FEATURE_REPO)


class InferenceRequest(BaseModel):
    driver_ids: List[int]


class InferenceResponse(BaseModel):
    prediction: Optional[float]
    error: Optional[str]


@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def predict(request: np.ndarray) -> np.ndarray:
    """
    Example request: [[0.5, 0.5, 500]]
    """
    Log().log.info(f"start predict")
    result = bentoml_runner.predict.run(request)
    Log().log.info(f"result: {result}")
    return result


@svc.api(
    input=JSON(pydantic_model=InferenceRequest),
    output=JSON(pydantic_model=InferenceResponse),
)
def inference(request: InferenceRequest, ctx: bentoml.Context) -> Dict[str, Any]:
    """
    Example request: {"driver_ids":[1001,1002,1003,1004,1005]}
    """
    Log().log.info(f"start inference")
    response = InferenceResponse()
    try:
        Log().log.info(f"request: {request}")
        driver_ids = request.driver_ids

        online_features = fs.get_online_features(
            entity_rows=[{"driver_id": driver_id} for driver_id in driver_ids],
            features=[f"driver_stats:{name}" for name in feature_list],
        )
        df = pd.DataFrame.from_dict(online_features.to_dict())
        Log().log.info(f"online features: {df}")

        input_features = df.drop(["driver_id"], axis=1)
        input_features = input_features[feature_list]
        Log().log.info(f"input_features: {input_features}")

        result = predict(input_features[sorted(input_features)])
        df["prediction"] = result
        best_driver_id = df["driver_id"].iloc[df["prediction"].argmax()]
        Log().log.info(f"best_driver_id: {best_driver_id}")

        response.prediction = best_driver_id
        ctx.response.status_code = 200

    except Exception as e:
        Log().log.error(f"error: {e}")
        response.error = str(e)
        ctx.response.status_code = 500

    Log().log.info(f"response: {response}")
    return response
