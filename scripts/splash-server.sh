#!/usr/bin/env bash

docker stop nfldata-splash-server
docker rm nfldata-splash-server
docker run \
  --publish 8050:8050 \
  --name nfldata-splash-server \
  scrapinghub/splash \
  --max-timeout 300
