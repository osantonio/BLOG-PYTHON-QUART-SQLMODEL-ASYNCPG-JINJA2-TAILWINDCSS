# app/routes/usuarios.py

from quart import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from sqlmodel import select, func
import math


# Importamos el modelo y la sesión de la base de datos
from app.models.usuario import Usuario
from app.config.database import get_session

# Creamos un Blueprint para las rutas de usuarios
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
async def listar():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    # Calculamos el offset
    offset = (page - 1) * per_page

    async with get_session() as session:
        # Modificamos la consulta para que use el offset y el límite
        query = select(Usuario).offset(offset).limit(per_page)
        result = await session.execute(query)
        usuarios = result.scalars().all()

        # ¡NUEVO PROBLEMA! Necesitamos el conteo total para los botones
        # Creamos una segunda consulta solo para contar
        count_query = select(func.count(Usuario.id))
        total_users = await session.scalar(count_query)
        # Calculamos el total de páginas, redondeando hacia arriba
        total_pages = math.ceil(total_users / per_page)
        
        return await render_template(
            'usuarios/listar.html',
            usuarios=usuarios,
            page=page,
            total_pages=total_pages
        )
    
@usuarios_bp.route('/crear', methods=['GET', 'POST'])
async def crear():
    """
    Ruta para mostrar el formulario de creación (GET) y
    para procesar la creación de un nuevo usuario (POST).
    """
    if request.method == 'POST':
        # Obtenemos el formulario
        form = await request.form
        # Obtenemos los datos del formulario que vamos a revisar
        username = form.get('username')
        email = form.get('email')
        password = form.get('password')
    
        # Verificamos si el email o username ya existen
        async with get_session() as session:
            verificar_email = select(Usuario).where(Usuario.email == email)
            if (await session.execute(verificar_email)).first():
                await flash(f"El correo electrónico '{email}' ya está registrado.", "error")
                return await render_template('usuarios/crear.html', form=form)
            
            verificar_username = select(Usuario).where(Usuario.username == username)
            if (await session.execute(verificar_username)).first():
                await flash(f"El nombre de usuario '{username}' ya está registrado.", "error")
                return await render_template('usuarios/crear.html', form=form)
        # Hasheamos la contraseña antes de guardarla
        hashear_contraseña = generate_password_hash(password)
        
        # Creamos una instancia del modelo Usuario con los datos del formulario
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            password=hashear_contraseña
        )
        
        session.add(nuevo_usuario)
        await session.commit()
        await flash(f"El usuario '{username}' ha sido registrado exitosamente.", "success")
        return redirect(url_for('usuarios.listar', form=form))
    
    # Si es una solicitud GET, mostramos el formulario vacío
    return await render_template('usuarios/crear.html', form={})

@usuarios_bp.route('/eliminar/<int:usuario_id>', methods=['POST'])
async def eliminar(usuario_id: int):
    """
    Ruta para eliminar un usuario por su ID.
    Solo acepta peticiones POST por seguridad.
    """
    async with get_session() as session:
        # Buscamos el usuario por su ID
        usuario = await session.get(Usuario, usuario_id)
        
        if usuario:
            # Si el usuario existe, lo eliminamos
            await session.delete(usuario)
            await session.commit()
            await flash(f"Usuario '{usuario.username}' eliminado correctamente.", "success")
        else:
            # Si el usuario no se encuentra
            await flash("El usuario no fue encontrado.", "error")
            
    # Redirigimos de vuelta a la lista de usuarios
    return redirect(url_for('usuarios.listar'))