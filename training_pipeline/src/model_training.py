import uuid

import mlflow
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from sklearn.linear_model import ElasticNet

from utils import *

Log(AppConst.MODEL_TRAINING)
AppPath()


def yield_artifacts(run_id, path=None):
    """Yield all artifacts in the specified run"""
    client = MlflowClient()
    for item in client.list_artifacts(run_id, path):
        if item.is_dir:
            yield from yield_artifacts(run_id, item.path)
        else:
            yield item.path


def fetch_logged_data(run_id):
    """Fetch params, metrics, tags, and artifacts in the specified run"""
    client = MlflowClient()
    data = client.get_run(run_id).data
    # Exclude system tags: https://www.mlflow.org/docs/latest/tracking.html#system-tags
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = list(yield_artifacts(run_id))
    return {
        "params": data.params,
        "metrics": data.metrics,
        "tags": tags,
        "artifacts": artifacts,
    }


def train_model():
    Log().log.info("start train_model")
    inspect_curr_dir()

    # Setup tracking server
    config = Config()
    Log().log.info(f"config: {config.__dict__}")
    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    mlflow.set_experiment(config.experiment_name)
    Log().log.info((mlflow.get_tracking_uri(), mlflow.get_artifact_uri()))
    mlflow.sklearn.autolog()

    # Load data
    train_x = load_df(AppPath.TRAIN_X_PQ)
    train_y = load_df(AppPath.TRAIN_Y_PQ)

    # Training
    model = ElasticNet(
        alpha=config.alpha,
        l1_ratio=config.l1_ratio,
        random_state=config.random_seed,
    )
    model.fit(train_x, train_y)

    # Log metadata
    mlflow.set_tag("mlflow.runName", str(uuid.uuid1())[:8])
    mlflow.log_param("alpha", config.alpha)
    mlflow.log_param("l1_ratio", config.l1_ratio)
    signature = infer_signature(train_x, model.predict(train_x))
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path=AppConst.MLFLOW_MODEL_PATH_PREFIX,
        signature=signature,
    )
    mlflow.end_run()

    # Inspect metadata
    run_id = mlflow.last_active_run().info.run_id
    Log().log.info("Logged data and model in run {}".format(run_id))
    for key, data in fetch_logged_data(run_id).items():
        Log().log.info("\n---------- logged {} ----------".format(key))
        Log().log.info(data)

    # Write latest run_id to file
    run_info = RunInfo(run_id)
    run_info.save()
    inspect_dir(run_info.path)


if __name__ == "__main__":
    train_model()
