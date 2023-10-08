#!/bin/bash

# Replace with the path to your virtual environment activation script
source deployed_project/scraper_owncloud_geomatique/scraper_owncloud_geomatique/bin/activate

# Navigate to your project directory
cd deployed_project/scraper_owncloud_geomatique

# Run your Python script
python3 main.py

# Deactivate the virtual environment
deactivate
