from utils import *
import mlflow

Log(AppConst.BATCH_PREDICTION)
AppPath()


def batch_prediction():
    Log().log.info("start batch_prediction")
    inspect_curr_dir()

    config = Config()

    # Download model
    registered_model_file = AppPath.ROOT / config.registered_model_file
    Log().log.info(f"registered_model_file: {registered_model_file}")
    registered_model_dict = load_json(registered_model_file)
    model_uri = registered_model_dict["_source"]

    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    mlflow_model = mlflow.pyfunc.load_model(model_uri=model_uri)

    # Load data
    batch_df = load_df(AppPath.BATCH_INPUT_PQ)
    preds = mlflow_model.predict(batch_df)
    batch_df["pred"] = preds

    Log().log.info("----- Example output -----")
    Log().log.info(batch_df.head())

    # Write preds to file
    to_parquet(batch_df, AppPath.BATCH_OUTPUT_PQ)
    inspect_dir(AppPath.BATCH_OUTPUT_PQ)


if __name__ == "__main__":
    batch_prediction()
