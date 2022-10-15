# Model serving

```bash
# Go to data pipeline and deploy feature repo
cd ../data_pipeline
make deploy_feature_repo
cd ../model_serving

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
