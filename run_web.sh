#!/bin/bash
# set -e : força o script a sair caso qqr erro ocorra
set -e

cd customers_api

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000
