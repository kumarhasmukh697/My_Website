#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

cd portfolio

python manage.py collectstatic --no-input
python manage.py migrate

if [ "${SEED_PORTFOLIO:-false}" = "true" ]; then
    python manage.py seed_portfolio
fi

if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
    python manage.py ensure_superuser
fi
