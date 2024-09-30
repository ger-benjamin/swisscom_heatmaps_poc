DOCKER_BASE = camptocamp/swisscom_heatmap_geoproxy
VENV_BIN = .venv/bin
GIT_HASH := $(shell git rev-parse HEAD)

.venv/timestamp: api/requirements.txt
	virtualenv --python=/usr/bin/python3 .venv
	${VENV_BIN}/pip install --upgrade pip
	${VENV_BIN}/pip install --upgrade -r api/requirements.txt
	touch $@

.PHONY: black-all
black-all: .venv/timestamp
	python3 ${VENV_BIN}/black api/swisscom_heatmap_geoproxy --check

.PHONY: build-api
build-api:
	docker build --tag=$(DOCKER_BASE)_wsgi:latest --build-arg "GIT_HASH=$(GIT_HASH)" api
