# app/config/database.py

# importamos las variables de entorno
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

import ssl
import os

load_dotenv()

# importamos la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')
# si la url de la base de datos no esta cargada correctamente:
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no esta configurada en las variables de entorno")

# creamos un contexto de seguridad ssl
ssl_context = ssl.create_default_context()

# motor de la base de datos asincrono con sqlalchemy
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context},
    echo=False # para ver las consultas sql en la consola
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)