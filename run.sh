#!/usr/bin/env bash
export FLASK_APP=app.server
export FLASK_ENV=development
python -m flask run --host=127.0.0.1 --port=8000