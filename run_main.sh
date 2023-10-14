#!/bin/bash
exec >> /path/to/logfile.log 2>&1

# path to virtual environment
venv_path="/home/ubuntu/deployed_project/scraper_owncloud_geomatique/scraper_venv/bin/activate"

# Check if the virtual environment path exists
if [ -f "$venv_path" ]; then
    echo "Activation environnemnet virtuel ..."
    source "$venv_path"

    echo "Execution de main.py"
    # Run Python script
    python3 /home/ubuntu/deployed_project/scraper_owncloud_geomatique/main.py

    echo "Desactivation environnement virutel"
    # Deactivate the virtual environment
    deactivate
else
    echo "Virtual environment not found at: $venv_path"
fi
