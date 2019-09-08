#!/bin/bash
set -e

cd customers_api

celery worker -A customers_api -l info
