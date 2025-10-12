#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start the application with uvicorn
# Azure sets the PORT environment variable
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
