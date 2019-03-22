#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir logs
touch logs/gunicorn.log
touch logs/access.log
tail -n 0 -f logs/*.log &

echo Starting nginx
echo Starting gnunicorn processes
exec gunicorn perp.app:app \
    -b unix:/tmp/gunicorn.sock \
    --workers 3 \
    --log-level=info \
    --log-file=logs/gunicorn.log \
    --access-logfile=logs/access.log &
exec service nginx start
