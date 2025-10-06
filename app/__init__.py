# ./app/__init__.py

# hacemos las importaciones necesarias
from quart import Quart
from app.config.database import create_db_and_tables
from zoneinfo import ZoneInfo
import dotenv
import os

# importamos las rutas
from app.routes.main import main_bp
from app.routes.usuarios import usuarios_bp

def localtime(value, tz_name='America/Bogota'):
    """
    Convierte una fecha y hora en la zona horaria especificada y la formatea como una cadena.
    
    Args:
        value (datetime.datetime): La fecha y hora a convertir.
        tz_name (str, optional): El nombre de la zona horaria. Por defecto es 'America/Bogota'.
    
    Returns:
        str: La fecha y hora convertida y formateada como una cadena.
    """
    if not value:
        return ""
    return value.astimezone(ZoneInfo(tz_name)).strftime("%d-%m-%Y %H:%M")


def create_app():
    app = Quart(__name__)

    # carga las variables de entorno desde el archivo .env
    dotenv.load_dotenv()
    
    # configuramos la zona horaria por defecto
    app.jinja_env.filters['localtime'] = localtime

    # configura la aplicacion con las variables de entorno
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    app.config['PORT'] = int(os.getenv('PORT', 5000))
    app.config['AUTO_RELOAD'] = os.getenv('AUTO_RELOAD', 'False').lower() == 'true'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')



    # manejo de los Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)
    
    # configura una funcion de inicializacion
    @app.before_serving
    async def startup():
        await create_db_and_tables()

    return app

