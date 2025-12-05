"""Validadores para datos de flags."""

import re
from typing import List
from sqlalchemy.orm import Session
from app.models.flag import Flag
from app.exceptions import (
    DuplicateFlagException,
    InvalidRolloutPercentageException,
    InvalidFlagNameException,
)


class FlagValidator:
    """Validador para datos de flags."""

    # Expresión regular para nombres de flags válidos
    NAME_PATTERN = re.compile(r"^[a-z0-9_-]+$")

    @staticmethod
    def validate_name_format(name: str) -> None:
        """
        Valida el formato del nombre de la flag.

        Args:
            name: Nombre de la flag a validar

        Raises:
            InvalidFlagNameException: Si el formato del nombre no es válido
        """
        if not name:
            raise InvalidFlagNameException("El nombre de la flag no puede estar vacío")

        if " " in name:
            raise InvalidFlagNameException(name)

        if not FlagValidator.NAME_PATTERN.match(name.lower()):
            raise InvalidFlagNameException(name)

    @staticmethod
    def validate_name_unique(db: Session, name: str, exclude_id: int = None) -> None:
        """
        Valida que el nombre de la flag sea único.

        Args:
            db: Sesión de base de datos
            name: Nombre de la flag a validar
            exclude_id: ID opcional de flag a excluir de la validación (para actualizaciones)

        Raises:
            DuplicateFlagException: Si ya existe una flag con ese nombre
        """
        query = db.query(Flag).filter(Flag.name == name.lower())

        if exclude_id is not None:
            query = query.filter(Flag.id != exclude_id)

        existing_flag = query.first()

        if existing_flag:
            raise DuplicateFlagException(name)

    @staticmethod
    def validate_rollout_percentage(percentage: int) -> None:
        """
        Valida el porcentaje de despliegue.

        Args:
            percentage: Porcentaje de despliegue a validar

        Raises:
            InvalidRolloutPercentageException: Si el porcentaje no está entre 0 y 100
        """
        if not isinstance(percentage, int):
            raise InvalidRolloutPercentageException(percentage)

        if percentage < 0 or percentage > 100:
            raise InvalidRolloutPercentageException(percentage)

    @staticmethod
    def validate_allowed_users(allowed_users: List[str]) -> None:
        """
        Valida el formato de los usuarios permitidos.

        Args:
            allowed_users: Lista de IDs de usuarios

        Raises:
            ValueError: Si el formato de allowed_users no es válido
        """
        if not isinstance(allowed_users, list):
            raise ValueError("allowed_users debe ser una lista")

        for user_id in allowed_users:
            if not isinstance(user_id, str):
                raise ValueError("Todos los IDs de usuario deben ser cadenas de texto")

            if not user_id.strip():
                raise ValueError("Los IDs de usuario no pueden estar vacíos")

    @staticmethod
    def validate_flag_data(
        db: Session,
        name: str,
        rollout_percentage: int,
        allowed_users: List[str],
        exclude_id: int = None,
    ) -> None:
        """
        Valida todos los datos de una flag

        Args:
            db: Sesión de base de datos
            name: Nombre de la flag
            rollout_percentage: Porcentaje de despliegue
            allowed_users: Lista de IDs de usuarios permitidos
            exclude_id: ID opcional de flag a excluir de la validación de unicidad
        """
        FlagValidator.validate_name_format(name)
        FlagValidator.validate_name_unique(db, name, exclude_id)
        FlagValidator.validate_rollout_percentage(rollout_percentage)
        FlagValidator.validate_allowed_users(allowed_users)
