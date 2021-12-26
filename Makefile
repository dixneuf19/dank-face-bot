.PHONY: install install-dev dev build run push release release-multi deploy

DOCKER_REPOSITERY=dixneuf19
IMAGE_NAME=dank-face-bot
IMAGE_TAG=$(shell git rev-parse --short HEAD)
DOCKER_IMAGE_PATH=$(DOCKER_REPOSITERY)/$(IMAGE_NAME):$(IMAGE_TAG)
APP_NAME=dank-face-bot
KUBE_NAMESPACE=dank-face-bot

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

dev:
	python main.py

format:
	isort .
	black .

check-format:
	isort --profile black --check .
	black --check .
	# flake8 .

build:
	docker build -t $(DOCKER_IMAGE_PATH) .

build-multi:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(DOCKER_IMAGE_PATH) .


run: build
	docker run -p 8000:80 --env-file=.env -v "$(shell pwd)/pictures/:/tmp/pictures" $(DOCKER_IMAGE_PATH)

push:
	docker push $(DOCKER_IMAGE_PATH)

release: build push

release-multi:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(DOCKER_IMAGE_PATH) . --push

secret:
	kubectl -n ${KUBE_NAMESPACE} create secret generic telegram-token --from-env-file=.env
