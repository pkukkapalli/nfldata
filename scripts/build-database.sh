#!/usr/bin/env bash

green_color="\033[0;32m"
red_color="\033[0;31m"
no_color="\033[0m"

function fail_spider {
  echo -e "${red_color}Spider failed: $1 could not finish successfully${no_color}"
  exit 1
}

rm logfiles/*.log && echo -e "Cleaning up logfiles"

spiders=()
while getopts "s:" OPTION; do
  case $OPTION in
  s)
    spiders+=($OPTARG)
    ;;
  *)
    echo "${red_color}Invalid option: $OPTION${no_color}"
    exit 1
    ;;
  esac
done

if [ ${#spiders[@]} -eq 0 ]; then
  spiders=(franchises teams stadiums schools executives front_office_members coaches coaching_staffs players roster_members injuries draft_picks)
fi

# Scrape data from the internet using Scrapy.
for spider in "${spiders[@]}"
do
  echo -e "${green_color}Spider running: ${spider}${no_color}"
  nfldata-env/bin/scrapy crawl --logfile "logfiles/${spider}.log" $spider || fail_spider $spider
done
