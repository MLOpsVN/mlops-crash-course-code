import mlflow
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from utils import *

Log(AppConst.MODEL_EVALUATION)
AppPath()


def eval_metrics(actual, pred):
    Log().log.info("start eval_metrics")
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    return rmse, mae


def evaluate_model():
    Log().log.info("start evaluate_model")
    inspect_curr_dir()

    run_info = RunInfo.load(AppPath.RUN_INFO)
    Log().log.info(f"loaded run_info {run_info.__dict__}")

    config = Config()
    Log().log.info(f"config: {config.__dict__}")
    mlflow.set_tracking_uri(config.mlflow_tracking_uri)

    model = mlflow.pyfunc.load_model(
        f"runs:/{run_info.run_id}/{AppConst.MLFLOW_MODEL_PATH_PREFIX}"
    )
    Log().log.info(f"loaded model {model.__dict__}")

    test_x = load_df(AppPath.TEST_X_PQ)
    test_y = load_df(AppPath.TEST_Y_PQ)

    predicted_qualities = model.predict(test_x)
    (rmse, mae) = eval_metrics(test_y, predicted_qualities)

    # Write evaluation result to file
    eval_result = EvaluationResult(rmse, mae)
    Log().log.info(f"eval result: {eval_result}")
    eval_result.save()
    inspect_dir(eval_result.path)


if __name__ == "__main__":
    evaluate_model()
