# app/routes/usuarios.py

from quart import Blueprint, render_template
from sqlmodel import select

# Importamos el modelo y la sesión de la base de datos
from app.models.usuario import Usuario
from app.config.database import get_session

# Creamos un Blueprint para las rutas de usuarios
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
async def listar():
    """
    Ruta para obtener y mostrar una lista de todos los usuarios registrados.
    """
    async with get_session() as session:
        # Creamos una consulta para seleccionar todos los usuarios
        query = select(Usuario)
        # Ejecutamos la consulta de forma asíncrona
        result = await session.execute(query)
        usuarios = result.all()
        
        # Renderizamos la plantilla y le pasamos la lista de usuarios
        return await render_template('usuarios/listar.html', usuarios=usuarios)