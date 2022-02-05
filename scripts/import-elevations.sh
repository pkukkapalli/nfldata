#!/usr/bin/env bash

green_color="\033[0;32m"
no_color="\033[0m"

echo -e "${green_color}Importing data into nfldata.sqlite${no_color}"
nfldata-env/bin/python -m nfldata.analysis.elevations
