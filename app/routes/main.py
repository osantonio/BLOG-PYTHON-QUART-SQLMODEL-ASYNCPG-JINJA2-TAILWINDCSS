# ./routes/main.py

# hacemos las importaciones necesarias
from quart import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
async def hello():
    return await render_template('index.html')
