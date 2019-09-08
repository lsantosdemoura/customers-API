#!/bin/bash
# set -e : forces script to exit if something goes wrong
set -e

cd customers_api

# checo se existe migracao por fazer
MIGRATIONS=`python manage.py makemigrations | wc -l `
[ ${MIGRATIONS}  != 1 ] && echo "YOU NEED TO MAKEMIGRATIONS AND COMMIT THEM" && exit 1

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
