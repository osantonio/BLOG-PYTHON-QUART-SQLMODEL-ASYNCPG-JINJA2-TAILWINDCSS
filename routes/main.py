# ./routes/main.py

# hacemos las importaciones necesarias
from quart import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
async def hello():
    return jsonify({'message': 'hello'})
