#!/bin/bash

python /code/manage.py test
python /code/manage.py loaddata /code/store_auth/fixture.json
python /code/manage.py migrate
python /code/manage.py runserver 0.0.0.0:8000