#!/usr/bin/env sh

docker stop nfldata-api
docker rm nfldata-api
docker build \
  --tag nfldata-api:local \
  --file containers/api.Dockerfile . || exit 1
docker run \
  --publish 5000:5000 \
  -v $(pwd)/nfldata.sqlite:/usr/src/app/nfldata.sqlite \
  --name nfldata-api \
  nfldata-api:local
