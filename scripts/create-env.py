#!/usr/bin/env python3
import subprocess
import argparse
import os
import venv


def pip_install(requirements_file):
    subprocess.call(['nfldata-env/bin/pip', 'install', '-r', requirements_file])


parser = argparse.ArgumentParser(
    description='create a virtual environment for this project')
parser.add_argument('--api',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--dev',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--notebook',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--spider',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--all',
                    default=False,
                    action=argparse.BooleanOptionalAction)

args = parser.parse_args()

if not os.path.exists('nfldata-env'):
    builder = venv.EnvBuilder(with_pip=True)
    builder.create('nfldata-env')

if args.api or args.all:
    pip_install('api-requirements.txt')

if args.dev or args.all:
    pip_install('dev-requirements.txt')

if args.notebook or args.all:
    pip_install('notebook-requirements.txt')

if args.spider or args.all:
    pip_install('spider-requirements.txt')
