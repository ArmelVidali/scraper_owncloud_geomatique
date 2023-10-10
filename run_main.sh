#!/bin/bash
exec >> /path/to/logfile.log 2>&1

# Active venv
echo "Activation environnemnet virtuel ..."
source /home/ubuntu/deployed_project/scraper_owncloud_geomatique/scraper_owncloud_geomatique/bin/activate

echo "Execution de main.py"
# Run your Python script
python3 /home/ubuntu/deployed_project/scraper_owncloud_geomatique/main.py

echo "Desactivation environnement virutel"
# Deactivate the virtual environment
deactivate
