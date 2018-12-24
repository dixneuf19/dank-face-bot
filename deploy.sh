#!/bin/bash

set -e

docker build -t gcr.io/${PROJECT_NAME_PRD}/${DOCKER_IMAGE_NAME}:${TRAVIS_COMMIT} .

gcloud --quiet config set project $PROJECT_NAME_PRD
gcloud --quiet config set container/cluster $CLUSTER_NAME_PRD
gcloud --quiet config set compute/zone ${CLOUDSDK_COMPUTE_ZONE}
gcloud --quiet container clusters get-credentials $CLUSTER_NAME_PRD

gcloud docker push gcr.io/${PROJECT_NAME_PRD}/${DOCKER_IMAGE_NAME}:${TRAVIS_COMMIT}

envsubst < kubernetes.template.yml > kubernetes.yml

kubectl apply -f kubernetes.yml

