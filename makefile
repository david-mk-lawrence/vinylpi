REPO:= vinylpi
IMG_TAG ?= latest
API_IMG := ${REPO}/api:${IMG_TAG}
WEB_IMG := ${REPO}/web:${IMG_TAG}

build:
	docker build --target api -t ${API_IMG} .
	docker build --target web -t ${WEB_IMG} .
