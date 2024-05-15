#!/bin/bash
echo "Starting Brussels worker"

conda run --no-capture-output -n es_tripadvisor_nyc celery -A celery_app worker --loglevel=INFO --autoscale=4,1
