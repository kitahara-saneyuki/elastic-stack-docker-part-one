#!/bin/bash
echo "Starting Brussels worker"

conda run --no-capture-output -n es_tripadvisor_nyc celery -A celery_app worker --pool=solo --loglevel=INFO
