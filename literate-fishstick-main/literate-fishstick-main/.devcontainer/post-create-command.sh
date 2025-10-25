#!/bin/bash
echo "Starting post-create setup..."

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate

echo "-------------------------------------------------------"
echo "✅ Setup complete!"
echo "To run the server, use the following command:"
echo "python manage.py runserver 0.0.0.0:8000"
echo "-------------------------------------------------------"
