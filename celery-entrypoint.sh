#!/bin/sh
cd ./notinder
celery -A notinder worker -l info