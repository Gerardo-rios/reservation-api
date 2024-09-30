#!/bin/bash

if [ -f .env ]; then
  export $(cat .env | xargs)
fi

VERSION=${1:-latest}

export VERSION

envsubst < k8s/secrets/secrets.yaml | kubectl apply -f -

kubectl apply -f k8s/mysql/mysql-pv.yaml

kubectl apply -f k8s/mysql/mysql-deployment.yaml

kubectl apply -f k8s/mysql/mysql-service.yaml

kubectl wait --for=condition=available --timeout=300s deployment/mysql-deployment

envsubst < k8s/api/fastapi-deployment.yaml | kubectl apply -f -

kubectl apply -f k8s/api/fastapi-service.yaml

envsubst < k8s/jobs/alembic-migration.yaml | kubectl apply -f -

kubectl wait --for=condition=complete --timeout=300s job/alembic-migration

echo "Deployment of version ${VERSION} completed!"

echo "You can access the FastAPI service at the following URL:"
minikube service fastapi-service --url