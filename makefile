REPO:= rfid-player
IMG_TAG ?= latest
IMG := $${USER}/${REPO}:${IMG_TAG}

build:
	docker build \
		-t ${IMG} .
