#!/bin/bash
# set -e : forces script to exit if something goes wrong
set -e

cd customers_api

if [ -z $1 ]; then
    # if it does not have arguments then ALL tests will run + coverage
    echo "Running complete test suite"
    export PYTHONPATH=$PWD
    export PYTHONDONTWRITEBYTECODE=1
    pytest --cov=.
else
    echo "Testing $@"
    pytest "$@"
fi
