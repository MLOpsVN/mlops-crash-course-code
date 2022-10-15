# Training pipeline

```bash
# Go to data pipeline and deploy feature repo
cd ../data_pipeline
make deploy_feature_repo
cd ../training_pipeline

# To test source files at local before running in Airflow
export TRAINING_PIPELINE_DIR="path/to/mlops-crash-course-code/training_pipeline"
cd src
python <source_file>

# Build
make build_image && make deploy_dags

# Go to airflow UI
# Set variable MLOPS_CRASH_COURSE_CODE_DIR=path/to/mlops-crash-course-code
# Run dags
```
