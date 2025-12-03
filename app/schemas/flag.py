"""Esquema de flags para validación de solicitudes/respuestas."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class FlagBase(BaseModel):
    """Esquema base para Flag con atributos comunes."""

    name: str = Field(..., min_length=1, max_length=100, description="Nombre único de la bandera")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la bandera")
    enabled: bool = Field(default=True, description="Indica si la bandera está habilitada")
    rollout_percentage: int = Field(default=0, ge=0, le=100, description="Porcentaje de despliegue (0-100)")
    allowed_users: List[str] = Field(default_factory=list, description="Lista de IDs de usuarios permitidos")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida el formato del nombre de la bandera."""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('El nombre de la bandera solo puede contener caracteres alfanuméricos, guiones y guiones bajos')
        if ' ' in v:
            raise ValueError('El nombre de la bandera no puede contener espacios')
        return v.lower()  # Normalizar a minúsculas


class FlagCreate(FlagBase):
    """Esquema para crear una nueva bandera."""
    pass


class FlagUpdate(BaseModel):
    """Esquema para actualizar una bandera existente."""

    description: Optional[str] = Field(None, max_length=500, description="Nueva descripción de la bandera")
    enabled: Optional[bool] = Field(None, description="Nuevo estado de habilitación")
    rollout_percentage: Optional[int] = Field(None, ge=0, le=100, description="Nuevo porcentaje de despliegue (0-100)")
    allowed_users: Optional[List[str]] = Field(None, description="Nueva lista de IDs de usuarios permitidos")


class FlagResponse(FlagBase):
    """Esquema para la respuesta de una bandera."""

    id: int = Field(..., description="ID único de la bandera")
    created_at: datetime = Field(..., description="Fecha y hora de creación")

    class Config:
        from_attributes = True


class FlagListResponse(BaseModel):
    """Esquema para la respuesta de lista de banderas."""

    flags: List[FlagResponse] = Field(..., description="Lista de banderas")
    total: int = Field(..., description="Número total de banderas")
    # /flags refleja el entorno
    environment: str = Field(..., description="Entorno actual")