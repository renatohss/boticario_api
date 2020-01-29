#!/bin/bash

export SECRET_KEY=RnxHufPHvJCI9q7G1bxI1j9FI93p0Y9W

echo "Activating venv..."
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=production
echo "Flask App: $FLASK_APP"
echo "Flask Environment: $FLASK_ENV"
echo "============================="
flask run