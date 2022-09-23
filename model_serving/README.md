# Model serving

```bash
# Go to data pipeline and deploy feature repo
cd ../data_pipeline
make deploy_feature_repo
cd ../training_pipeline

# Go to training pipeline and deploy registered model file
cd ../training_pipeline
make deploy_registered_model_file
cd ../model_serving

# Clone .env-example and rename to .env in both model_serving and model_serving/deployment folders

# To test source files at local before running in Airflow
cd feature_repo
feast apply
cd ..

export MODEL_SERVING_DIR="path/to/mlops-crash-course-code/model_serving"
cd src
python <source_file>

# Build
make build_image && make deploy_dags

# Run batch serving
# Go to airflow UI
# Set variable MLOPS_CRASH_COURSE_CODE_DIR=path/to/mlops-crash-course-code
# Run dags

# Run online serving
make compose_up
# To shutdown online serving
make compose_down
```
