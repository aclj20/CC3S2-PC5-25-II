"""Manejadores globales de excepciones para la aplicación."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.exceptions import (
    FlagNotFoundException,
    DuplicateFlagException,
    InvalidRolloutPercentageException,
    InvalidFlagNameException,
    FlagException
)
import logging

logger = logging.getLogger(__name__)


def add_exception_handlers(app):
    """
    Agrega manejadores de excepciones a la aplicación FastAPI.
    
    Args:
        app: Instancia de la aplicación FastAPI
    """
    
    @app.exception_handler(FlagNotFoundException)
    async def flag_not_found_handler(request: Request, exc: FlagNotFoundException):
        """Maneja la excepción FlagNotFoundException."""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Flag no encontrada",
                "message": exc.message,
                "flag_name": exc.flag_name
            }
        )
    
    @app.exception_handler(DuplicateFlagException)
    async def duplicate_flag_handler(request: Request, exc: DuplicateFlagException):
        """Maneja la excepción DuplicateFlagException."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Flag duplicada",
                "message": exc.message,
                "flag_name": exc.flag_name
            }
        )
    
    @app.exception_handler(InvalidRolloutPercentageException)
    async def invalid_rollout_handler(request: Request, exc: InvalidRolloutPercentageException):
        """Maneja la excepción InvalidRolloutPercentageException."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Porcentaje de implementación no válido",
                "message": exc.message,
                "value": exc.value
            }
        )
    
    @app.exception_handler(InvalidFlagNameException)
    async def invalid_name_handler(request: Request, exc: InvalidFlagNameException):
        """Maneja la excepción InvalidFlagNameException."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Nombre de flag no válido",
                "message": exc.message,
                "name": exc.name,
                "suggestion": "Use solo caracteres alfanuméricos en minúsculas, guiones y guiones bajos. No se permiten espacios."
            }
        )
    
    @app.exception_handler(FlagException)
    async def flag_exception_handler(request: Request, exc: FlagException):
        """Maneja excepciones genéricas de FlagException."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Error de flag",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Maneja errores de validación de Pydantic."""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Error de Validación",
                "message": "Datos de solicitud no válidos",
                "details": errors
            }
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """Maneja errores de integridad de SQLAlchemy."""
        logger.error(f"Error de integridad de la base de datos: {exc}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Violación de restricción de base de datos",
                "message": "La operación viola una restricción de la base de datos. Podría ser una entrada duplicada."
            }
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Maneja cualquier excepción no controlada."""
        logger.error(f"Excepción no controlada: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Error Interno del Servidor",
                "message": "Ocurrió un error inesperado. Por favor, intente nuevamente más tarde."
            }
        )