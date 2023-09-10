#!/bin/sh
cd ./notinder  # Замените на актуальный путь к вашей поддиректории notinder
celery -A notinder worker -l info
