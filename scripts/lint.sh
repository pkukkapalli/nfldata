#!/usr/bin/env sh

nfldata-env/bin/pylint nfldata
npm run lint --prefix webapp
