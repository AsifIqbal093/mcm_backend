#!/bin/bash
cd ~/home/mcm_backend

# Activate virtual environment
source venv/bin/activate

# Pull the latest changes
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application (modify this based on your setup)
touch tmp/restart.txt

echo "Deployment completed!"
