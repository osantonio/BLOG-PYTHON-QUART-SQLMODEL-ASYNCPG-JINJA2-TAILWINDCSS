# ./app/__init__.py

# hacemos las importaciones necesarias
from quart import Quart
from app.config.database import create_db_and_tables

# importamos las rutas
from app.routes.main import main_bp
from app.routes.usuarios import usuarios_bp



def create_app():
    app = Quart(__name__)

    # manejo de los Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)
    
    # configura una funcion de inicializacion
    @app.before_serving
    async def startup():
        await create_db_and_tables()

    return app

