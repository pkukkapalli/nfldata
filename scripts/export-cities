#!/usr/bin/env bash

green_color="\033[0;32m"
red_color="\033[0;31m"
no_color="\033[0m"

output_file="cities.csv"
while getopts "o:" OPTION; do
  case $OPTION in
  o)
    output_file=$OPTARG
    ;;
  *)
    echo "${red_color}Invalid option: $OPTION${no_color}"
    exit 1
    ;;
  esac
done

query="select city, state from stadiums where city is not null and state is not null group by city, state;"

sqlite3 -header -csv nfldata.sqlite "$query" > $output_file
