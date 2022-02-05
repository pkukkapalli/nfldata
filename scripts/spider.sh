#!/usr/bin/env sh

docker stop nfldata-spider
docker rm nfldata-spider
docker build \
  --tag nfldata-spider:local \
  --file containers/spider.Dockerfile . || exit 1
docker run \
  --net host \
  -v $(pwd)/nfldata.sqlite:/usr/src/app/nfldata.sqlite \
  -v $(pwd)/logfiles:/usr/src/app/logfiles \
  -v $(pwd)/.scrapy:/usr/src/app/.scrapy \
  --env "NFLDATA_USER_AGENT=nfldata (pradyothkukkapalli.com)" \
  nfldata-spider:local
