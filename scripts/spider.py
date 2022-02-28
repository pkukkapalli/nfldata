#!/usr/bin/env python3
import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description='run a scrapy spider')
parser.add_argument('spider', type=str)
parser.add_argument('--dev',
                    default=False,
                    action=argparse.BooleanOptionalAction)

args = parser.parse_args()

if not args.spider:
    print('Please specify a spider')
    exit(1)

try:
    os.remove(f'logfiles/{args.spider}.log')
except FileNotFoundError:
    print(f'No log file found for {args.spider}')

if args.dev:
    subprocess.call([
        'nfldata-env/bin/scrapy', 'crawl', '--logfile',
        f'logfiles/{args.spider}.log', args.spider
    ])
else:
    subprocess.call(['docker', 'stop', 'nfldata-spider'])
    subprocess.call(['docker', 'rm', 'nfldata-spider'])
    subprocess.check_call([
        'docker', 'builder', '--tag', 'nfldata-spider:local', '--file',
        'containers/spider.Dockerfile'
    ])
    subprocess.call([
        'docker', 'run', '--net', 'host', '-v',
        '$(pwd)/nfldata.sqlite:/usr/src/app/nfldata.sqlite', '-v',
        '$(pwd)/logfiles:/usr/src/app/logfiles', '-v',
        '$(pwd)/.scrapy:/usr/src/app/.scrapy', '--env',
        'NFLDATA_USER_AGENT=nfldata (pradyothkukkapalli.com)',
        'nfldata-spider:local', 'nfldata-env/bin/scrapy', 'crawl', '--logfile',
        f'logfiles/{args.spider}.log', args.spider
    ])
