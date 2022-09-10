# Training pipeline

```bash
# Go to data pipeline and deploy feature repo
cd ../data_pipeline
make deploy_feature_repo
cd ../training_pipeline

# Clone .env-example and rename to .env

# Build
make build_image && make deploy_dags

# Go to airflow UI and run dags
```
