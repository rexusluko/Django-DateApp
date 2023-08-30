#!/bin/sh

# Apply database migrations
python notinder/manage.py makemigrations date_app
python notinder/manage.py migrate

# Create Zodiac Signs and Compatibilities
python notinder/manage.py create_zodiac_signs
python notinder/manage.py create_compatibilities

# Create superuser
python notinder/manage.py create_super_user --username=admin --email=myemail@example.com --password=1234
python -m pytest notinder
python notinder/manage.py runserver 0.0.0.0:8000