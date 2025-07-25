#!/bin/bash
CURRENT_TIME=$(date "+%Y%m%d%H%M%S")
echo $CURRENT_TIME

docker build -f Dockerfile.deps -t infiniflow/ragflow_deps .

docker build --build-arg LIGHTEN=1 --build-arg NEED_MIRROR=1  -t ragflow-base:1.0 -f Dockerfile.base .
docker push my-registry/ragflow-base:1.0
docker build --build-arg LIGHTEN=1 --build-arg NEED_MIRROR=1  -t ragflow-base-uv:1.0 -f Dockerfile.base.uv .
docker push my-registry/ragflow-base-uv:1.0
docker build --build-arg NEED_MIRROR=1 --build-arg LIGHTEN=1 -t ragflow:$CURRENT_TIME -f Dockerfile.cicd .
docker build --build-arg NEED_MIRROR=1 --build-arg LIGHTEN=1 -t ragflow:$CURRENT_TIME -f Dockerfile.cicd.uv .