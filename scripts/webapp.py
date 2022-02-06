#!/usr/bin/env python3
import subprocess
import argparse

parser = argparse.ArgumentParser(description='start an instance of the webapp')
parser.add_argument('--dev',
                    default=False,
                    action=argparse.BooleanOptionalAction)

args = parser.parse_args()

if args.dev:
    subprocess.call(['npm', 'start', '--prefix', 'webapp'])
else:
    subprocess.call(['docker', 'stop', 'nfldata-webapp'])
    subprocess.call(['docker', 'rm', 'nfldata-webapp'])
    subprocess.check_call([
        'docker', 'build', '--tag', 'nfldata-webapp:local', '--file',
        'containers/webapp.Dockerfile', '.'
    ])
    subprocess.check_call([
        'docker', 'run', '--name', 'nfldata-webapp', '--publish', '3000:80',
        'nfldata-webapp:local'
    ])
