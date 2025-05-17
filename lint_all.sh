#!/bin/bash

echo "Running black..."
black . --exclude 'venv|__pycache__'

echo "Running isort..."
isort . --skip venv --skip __pycache__

echo "Running flake8..."
flake8 . --exclude=venv,__pycache__