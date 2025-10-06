from typing import Optional
from sqlmodel import Field, SQLModel, Column, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo

def colombia_now():
    """Devuelve la hora actual en zona horaria de Colombia."""
    return datetime.now(ZoneInfo("America/Bogota"))

class TimestampModel(SQLModel):
    """
    Modelo base con campos de creación y actualización en hora Colombia (UTC−5).
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=colombia_now)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=colombia_now, onupdate=colombia_now)
    )
