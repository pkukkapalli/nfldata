#!/usr/bin/env python3
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description='start an instance of the API server')
parser.add_argument('--dev',
                    default=False,
                    action=argparse.BooleanOptionalAction)

args = parser.parse_args()

if args.dev:
    subprocess.call(['nfldata-env/bin/flask', 'run'],
                    env={
                        'FLASK_APP': 'nfldata.api',
                        'FLASK_ENV': 'development'
                    })
else:
    subprocess.call(['docker', 'stop', 'nfldata-api'])
    subprocess.call(['docker', 'rm', 'nfldata-api'])
    subprocess.check_call([
        'docker', 'build', '--tag', 'nfldata-api:local', '--file',
        'containers/api.Dcokerfile', '.'
    ])
    subprocess.call([
        'docker', 'run', '--publish', '5000:5000', '-v',
        '$(pwd)/nfldata.sqlite:/usr/src/app/nfldata.sqlite', '--name',
        'nfldata-api', 'nfldata-api:local'
    ])
