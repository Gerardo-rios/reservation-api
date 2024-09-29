#!/bin/bash

kubectl apply -f k8s/secrets/secrets.yaml

kubectl apply -f k8s/mysql/mysql-pv.yaml

kubectl apply -f k8s/mysql/mysql-deployment.yaml
kubectl apply -f k8s/mysql/mysql-service.yaml

kubectl wait --for=condition=available --timeout=300s deployment/mysql-deployment

kubectl apply -f k8s/api/fastapi-deployment.yaml
kubectl apply -f k8s/api/fastapi-service.yaml

kubectl apply -f k8s/jobs/alembic-migration.yaml

kubectl wait --for=condition=complete --timeout=300s job/alembic-migration

echo "Deployment completed!"