"""Definición del modelo Flag"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class Flag(Base):
    """
    Feature Flag model.

    Atributos:
        id: Clave primaria
        name: Nombre único de la bandera (identificador)
        description: Descripción legible
        enabled: Indica si la bandera está habilitada
        rollout_percentage: Porcentaje de usuarios que recibirán la característica (0-100)
        allowed_users: Lista de IDs de usuarios que siempre obtienen la característica
        created_at: Marca de tiempo de creación de la bandera
    """

    __tablename__ = "flags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    rollout_percentage = Column(Integer, default=0, nullable=False)
    allowed_users = Column(JSON, default=list, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Flag(name='{self.name}', enabled={self.enabled}, rollout={self.rollout_percentage}%)>"
