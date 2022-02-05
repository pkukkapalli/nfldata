FROM python:3.9 as builder

WORKDIR /usr/src/app

COPY api-requirements.txt .
COPY scripts/create-env.py scripts/create-env.py

RUN scripts/create-env.py --api

FROM python:3.9-slim

WORKDIR /usr/src/app

COPY nfldata nfldata
COPY --from=builder /usr/src/app/nfldata-env nfldata-env

EXPOSE 5000

CMD ["nfldata-env/bin/gunicorn", "-b", "0.0.0.0:5000", "nfldata.api:app"]
