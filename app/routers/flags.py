"""Router para operaciones CRUD de flags."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.flag import Flag
from app.schemas.flag import FlagCreate, FlagUpdate, FlagResponse, FlagListResponse
from app.validators.flag_validator import FlagValidator
from app.exceptions import FlagNotFoundException

router = APIRouter(
    prefix="/api/flags",
    tags=["flags"]
)


@router.get("", response_model=FlagListResponse, status_code=status.HTTP_200_OK)
def list_flags(db: Session = Depends(get_db)):
    """
    Lista todas las flags.
    
    Returns:
        FlagListResponse: Lista de todas las flags con el conteo total
    """
    flags = db.query(Flag).all()
    return FlagListResponse(
        flags=flags,
        total=len(flags)
    )


@router.post("", response_model=FlagResponse, status_code=status.HTTP_201_CREATED)
def create_flag(flag_data: FlagCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva flag.
    
    Args:
        flag_data: Datos para la creación de la flag
        db: Sesión de base de datos
        
    Returns:
        FlagResponse: Flag creada
        
    Raises:
        DuplicateFlagException: Si ya existe una bandera con ese nombre
        InvalidRolloutPercentageException: Si el porcentaje de despliegue no es válido
        InvalidFlagNameException: Si el formato del nombre no es válido
    """
    # Validate flag data
    FlagValidator.validate_flag_data(
        db=db,
        name=flag_data.name,
        rollout_percentage=flag_data.rollout_percentage,
        allowed_users=flag_data.allowed_users
    )
    
    # Create flag
    db_flag = Flag(
        name=flag_data.name.lower(),
        description=flag_data.description,
        enabled=flag_data.enabled,
        rollout_percentage=flag_data.rollout_percentage,
        allowed_users=flag_data.allowed_users
    )
    
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    
    return db_flag


@router.get("/{flag_name}", response_model=FlagResponse, status_code=status.HTTP_200_OK)
def get_flag(flag_name: str, db: Session = Depends(get_db)):
    """
    Obtiene una bandera específica por su nombre.
    
    Args:
        flag_name: Nombre de la bandera
        db: Sesión de base de datos
        
    Returns:
        FlagResponse: Detalles de la bandera
        
    Raises:
        FlagNotFoundException: Si la bandera no existe
    """
    db_flag = db.query(Flag).filter(Flag.name == flag_name.lower()).first()
    
    if not db_flag:
        raise FlagNotFoundException(flag_name)
    
    return db_flag


@router.put("/{flag_name}", response_model=FlagResponse, status_code=status.HTTP_200_OK)
def update_flag(flag_name: str, flag_data: FlagUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una bandera existente.
    
    Args:
        flag_name: Nombre de la flag a actualizar
        flag_data: Datos actualizados de la bandera
        db: Sesión de base de datos
        
    Returns:
        FlagResponse: Flag actualizada
        
    Raises:
        FlagNotFoundException: Si la bandera no existe
        InvalidRolloutPercentageException: Si el porcentaje de despliegue no es válido
    """
    db_flag = db.query(Flag).filter(Flag.name == flag_name.lower()).first()
    
    if not db_flag:
        raise FlagNotFoundException(flag_name)
    
    # Validar el porcentaje de despliegue si se proporciona
    if flag_data.rollout_percentage is not None:
        FlagValidator.validate_rollout_percentage(flag_data.rollout_percentage)
    
    # Validar los usuarios permitidos si se proporcionan
    if flag_data.allowed_users is not None:
        FlagValidator.validate_allowed_users(flag_data.allowed_users)
    
    # Actualizar campos
    update_data = flag_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_flag, field, value)
    
    db.commit()
    db.refresh(db_flag)
    
    return db_flag