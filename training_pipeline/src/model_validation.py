"""
Reference: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

Model validation: The model is confirmed to be adequate for deployment—that its predictive performance is better than a certain baseline. This step occurs after you successfully train the model given the new data. You evaluate and validate the model before it's promoted to production. This offline model validation step consists of the following.

Producing evaluation metric values using the trained model on a test dataset to assess the model's predictive quality.

Comparing the evaluation metric values produced by your newly trained model to the current model, for example, production model, baseline model, or other business-requirement models. You make sure that the new model produces better performance than the current model before promoting it to production.

Making sure that the performance of the model is consistent on various segments of the data. For example, your newly trained customer churn model might produce an overall better predictive accuracy compared to the previous model, but the accuracy values per customer region might have large variance.
Making sure that you test your model for deployment, including infrastructure compatibility and consistency with the prediction service API.
"""

import mlflow
from utils import *

Log(AppConst.MODEL_VALIDATION)
AppPath()


def validate_model():
    Log().log.info("start validate_model")
    inspect_curr_dir()

    eval_result = EvaluationResult.load(AppPath.EVALUATION_RESULT)
    Log().log.info(f"loaded eval_result {eval_result}")

    errors = []
    config = Config()
    if eval_result.rmse > config.rmse_threshold:
        errors.append(
            f"rmse result {eval_result.rmse} exceeds threshold {config.rmse_threshold}"
        )
    if eval_result.mae > config.mae_threshold:
        errors.append(
            f"mae result {eval_result.mae} exceeds threshold {config.mae_threshold}"
        )

    if len(errors) > 0:
        Log().log.info(f"Model validation fails, will not register model: {errors}")
        return

    Log().log.info(f"Model validation succeeds, registering model")
    run_info = RunInfo.load(AppPath.RUN_INFO)
    Log().log.info(f"loaded run_info {run_info}")
    result = mlflow.register_model(
        f"runs:/{run_info.run_id}/{AppConst.MLFLOW_MODEL_PATH_PREFIX}",
        config.registered_model_name,
    )
    dump_json(result.__dict__, AppPath.REGISTERED_MODEL_VERSION)
    inspect_dir(AppPath.REGISTERED_MODEL_VERSION)


if __name__ == "__main__":
    validate_model()
