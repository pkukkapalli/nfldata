FROM python:3.9 as builder

WORKDIR /usr/src/app

COPY spider-requirements.txt .
COPY scripts/create-env.py scripts/create-env.py

RUN scripts/create-env.py --spider

FROM python:3.9-slim

WORKDIR /usr/src/app

COPY nfldata nfldata
COPY scrapy.cfg .
COPY scripts/build-database.sh scripts/build-database.sh
COPY --from=builder /usr/src/app/nfldata-env nfldata-env

CMD ["scripts/build-database.sh"]
