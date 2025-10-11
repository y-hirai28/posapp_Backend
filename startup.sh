#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start the application with uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000
