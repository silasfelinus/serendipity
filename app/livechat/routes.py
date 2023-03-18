from flask import render_template
from . import livechat_bp

@livechat_bp.route('/')
def livechat():
    return render_template('livechat.html')