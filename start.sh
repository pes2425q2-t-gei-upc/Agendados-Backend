#!/bin/bash
python manage.py migrate
python manage.py importer
daphne -b 0.0.0.0 -p 8080 agendadosDjango.asgi:application