#!/usr/bin/env bash

# Get the parent directory of where this script is.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
DIR="$( cd -P "$( dirname "$SOURCE" )/.." && pwd )"

# Change into that directory
cd "$DIR"

rm -rf __pycache__/
rm -rf build/
rm -rf venv/
rm -rf ftpctl.egg-info/
find . -name "*.pyc" -exec rm {} +

virtualenv -p /usr/local/bin/python3 venv
venv/bin/pip install -r requirements.txt
venv/bin/pip install -r requirements-build.txt
venv/bin/pip install --no-deps .
venv/bin/pyinstaller ftpctl.spec
