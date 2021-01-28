PYTHON_VERSION := 3.9
TAG := dev

build:
	docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} -t colabtomd:${TAG} .

build-dev:
	docker build \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		-t colabtomd_dev:${TAG} .

# Usage
# 	make run filename=some-file.ipynb dir=path/to/some/dir
run: build-dev
	docker run -v ${dir}:/data -w /data colabtomd_dev:dev --filename=${filename}