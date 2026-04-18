#!/bin/bash
docker build -t dedlin -f Dockerfile_local .
docker run --rm dedlin "$@"
