# ./app/__init__.py

# hacemos las importaciones necesarias
from quart import Quart

def create_app():
    app = Quart(__name__)

    # importamos las rutas
    from routes.main import main_bp

    # manejo de los Blueprints
    app.register_blueprint(main_bp)

    return app

