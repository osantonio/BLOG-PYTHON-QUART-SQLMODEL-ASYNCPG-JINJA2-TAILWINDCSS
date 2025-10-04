# ./app/models/usuario.py

from typing import Optional
from sqlmodel import Field
from app.models.utils import TimestampModel

class Usuario(TimestampModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True, max_length=100)
    password: str = Field(max_length=255)
    es_activo: bool = Field(default=True)