python3.8 -m venv venv

#Activate the virtual environment:
source ./venv/Scripts/activate

pip install -r requirements.txt
source ./.env
cd app
gradio main.py