# app/models/utils.py

from datetime import datetime
from typing import Optional
import pytz
from sqlalchemy import func
from sqlmodel import Field, SQLModel

# Definimos la zona horaria de Bogotá
BOGOTA_TIMEZONE = pytz.timezone('America/Bogota')

def get_bogota_time():
    """Función para obtener la hora actual en la zona horaria de Bogotá."""
    return datetime.now(BOGOTA_TIMEZONE)

class TimestampModel(SQLModel):
    """
    Un modelo base que incluye campos de timestamp para la fecha de creación y actualización.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        default_factory=get_bogota_time,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()}
    )

    updated_at: datetime = Field(
        default_factory=get_bogota_time,
        nullable=False,
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()}
    )