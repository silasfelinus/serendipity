#/bin/bash
source venv/Scripts/activate
pip install -r requirements.txt
source ./.env
python -m main.py