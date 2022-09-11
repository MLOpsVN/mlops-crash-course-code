# Training pipeline

```bash
# Go to data pipeline and deploy feature repo
cd ../data_pipeline
make deploy_feature_repo
cd ../training_pipeline

# Clone .env-example and rename to .env in both training_pipeline and training_pipeline/deployment folders

# To test source files at local before running in Airflow
export TRAINING_PIPELINE_DIR="path/to/mlops-crash-course-code/training_pipeline"
cd src
python <source_file>

# Build
make build_image && make deploy_dags

# Go to airflow UI
# Set variable TRAINING_PIPELINE_DIR=path/to/mlops-crash-course-code/training_pipeline
# Run dags
```
