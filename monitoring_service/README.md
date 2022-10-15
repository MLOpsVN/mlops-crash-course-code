# Monitoring service

```bash
# Go to data pipeline and deploy feature repo
cd ../data_pipeline
make deploy_feature_repo
cd ../monitoring_service

# Build
make build_image

# Run monitoring service
make compose_up
# To shutdown monitoring service
make compose_down

# To run mock_request.py
export MONITORING_SERVICE_DIR="path/to/mlops-crash-course-code/monitoring_service"
python src/mock_request.py -d normal -n 5
python src/mock_request.py -d drift -n 5
```
