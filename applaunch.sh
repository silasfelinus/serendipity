conda create -n visgpt python=3.8
conda activate visgpt
pip install -r requirements.txt
source ./.env
cd app
gradio main.py