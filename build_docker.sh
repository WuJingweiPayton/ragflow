#!/bin/bash
docker build -f Dockerfile.deps -t infiniflow/ragflow_deps .

docker build --build-arg LIGHTEN=1 --build-arg NEED_MIRROR=1  -t ragflow-base:1.0 -f Dockerfile.base .
docker push my-registry/ragflow-base:1.0
docker build --build-arg NEED_MIRROR=1 --build-arg LIGHTEN=1 -t ragflow:latest -f Dockerfile.cicd .
