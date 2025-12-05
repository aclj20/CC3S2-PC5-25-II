"""Servicio de evaluación de feature flags con reglas de segmentación."""

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.flag import Flag


class EvaluationService:
    """
    Servicio para evaluar si un usuario debe recibir una feature flag.

    Implementa tres estrategias de segmentación:
    1. Por usuario específico (allowed_users)
    2. Por porcentaje de rollout (rollout_percentage)
    3. Por estrategia predeterminada (flag enabled/disabled)
    """

    @staticmethod
    def evaluate_flag(flag: "Flag", user_id: str) -> tuple[bool, str]:
        """
        Evalúa si un usuario debe recibir la feature flag.

        Args:
            flag: Objeto Flag a evaluar
            user_id: ID del usuario

        Returns:
            tuple[bool, str]: (habilitado, razón)
                - habilitado: True si el usuario debe recibir la feature
                - razón: Explicación de por qué se otorgó o denegó
        """
        # Extraer valores de las columnas de SQLAlchemy
        # type: ignore se usa porque en runtime estos son valores Python normales,
        # no objetos Column de SQLAlchemy
        enabled = bool(flag.enabled) if flag.enabled is not None else False  # type: ignore[arg-type]
        allowed_users_list = list(flag.allowed_users) if flag.allowed_users else []  # type: ignore[arg-type,call-overload]
        rollout = int(flag.rollout_percentage) if flag.rollout_percentage is not None else 0  # type: ignore[arg-type,call-overload]
        flag_name = str(flag.name)

        # Regla 1: Si la flag está deshabilitada, nadie la recibe
        if not enabled:
            return False, "flag_disabled"

        # Regla 2: Usuarios en la lista de permitidos siempre reciben la feature
        if user_id in allowed_users_list:
            return True, "user_in_allowlist"

        # Regla 3: Evaluación por porcentaje de rollout
        if rollout > 0:
            # Usar hash determinístico para asegurar consistencia
            # El mismo usuario siempre obtendrá el mismo resultado para la misma flag
            user_hash = EvaluationService._hash_user_flag(user_id, flag_name)

            # Convertir hash a porcentaje (0-100)
            user_percentage = user_hash % 100

            if user_percentage < rollout:
                return True, "rollout_percentage"
            else:
                return False, "not_in_rollout_percentage"

        # Regla 4: Si no hay rollout y el usuario no está en allowlist, denegar
        return False, "default_deny"

    @staticmethod
    def _hash_user_flag(user_id: str, flag_name: str) -> int:
        """
        Genera un hash determinístico basado en user_id y flag_name.

        Args:
            user_id: ID del usuario
            flag_name: Nombre de la flag

        Returns:
            int: Valor hash como entero
        """
        # Crear una cadena única combinando user_id y flag_name
        unique_string = f"{user_id}:{flag_name}"

        # Generar hash SHA-256
        hash_object = hashlib.sha256(unique_string.encode())

        # Convertir los primeros 8 bytes del hash a un entero
        hash_int = int.from_bytes(hash_object.digest()[:8], byteorder="big")

        return hash_int
