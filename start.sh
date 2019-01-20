#!/usr/bin/env bash
gunicorn app:app -k gevent --worker-connections 1000 -b 0.0.0.0:5000 --log-file $LOG_PATH --log-level DEBUG