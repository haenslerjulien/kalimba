#!/bin/bash

until nc -z db 3306; do
  echo "Waiting for database ..."
  sleep 1
done

echo "building leaderboard ..."
python manage.py build_leaderboard

python manage.py runserver 0.0.0.0:8000