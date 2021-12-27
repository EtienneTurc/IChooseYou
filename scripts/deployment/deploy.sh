#!/bin/bash

source venv/bin/activate
PYTHON_ALIAS=python3.9 make install
python3.9 -m pip freeze > requirements.txt
deactivate
serverless deploy
