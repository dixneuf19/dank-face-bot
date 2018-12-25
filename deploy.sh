#!/bin/bash

set -e

docker build -t gcr.io/${PROJECT_NAME}/${DOCKER_IMAGE_NAME}:${TRAVIS_COMMIT} .

docker push gcr.io/${PROJECT_NAME}/${DOCKER_IMAGE_NAME}:${TRAVIS_COMMIT}

envsubst < kubernetes.template.yml > kubernetes.yml

kubectl config view
kubectl config current-context
kubectl apply -f kubernetes.yml

