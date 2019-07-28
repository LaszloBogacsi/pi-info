#!/bin/bash -e

if [ -f pipenv shell ]; then
    echo   "Load Python virtualenv"
fi
exec "$@"