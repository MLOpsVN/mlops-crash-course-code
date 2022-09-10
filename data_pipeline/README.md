# Data pipeline

```bash
# Clone .env-example and rename to .env

# Create/update feature store
make feast_apply

# Build
make build_image && make deploy_dags

# Go to airflow UI and run dags

# Deploy feature repo to training pipeline
make deploy_feature_repo
```
