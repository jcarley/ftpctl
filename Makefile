
# Metadata about this makefile and position
MKFILE_PATH := $(lastword $(MAKEFILE_LIST))
CURRENT_DIR := $(dir $(realpath $(MKFILE_PATH)))
CURRENT_DIR := $(CURRENT_DIR:/=)
PROJECT := $(notdir $(CURRENT_DIR))

build-linux:
	@docker build -t ${PROJECT}:latest .
	@docker run --rm -v ${CURRENT_DIR}:/app -w /app ${PROJECT}:latest scripts/build.sh
	@mkdir -p dist/linux
	@mv dist/ftpctl dist/linux/ftpctl-linux-x64

build-osx:
	@scripts/build.sh
	@mkdir -p dist/osx
	@mv dist/ftpctl dist/osx/ftpctl-darwin-x64

run:
	@docker run -it --rm -v ${CURRENT_DIR}:/app -v /var/run/docker.sock:/var/run/docker.sock -w /app ${PROJECT}:latest /bin/bash

cleanup:
	@docker rmi $(docker images --quiet --filter "dangling=true")

.PHONY: build-linux build-osx run cleanup
