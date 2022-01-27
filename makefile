REPO:= vinylpi
IMG_TAG ?= latest
API_IMG := ${REPO}/api:${IMG_TAG}
WEB_IMG := ${REPO}/web:${IMG_TAG}

build:
	docker build \
		-t ${IMG} .
