conda create -n serendipity python=3.8
conda activate serendipity
pip install -r requirements.txt
source ./.env
cd app
gradio main.py