# Data pipeline

```bash
# Create/update feature store
make feast_apply

# Build
make build_image && make deploy_dags

# Go to airflow UI
# Set variable MLOPS_CRASH_COURSE_CODE_DIR=path/to/mlops-crash-course-code
# Run dags

# Deploy feature repo to training pipeline
make deploy_feature_repo
```
