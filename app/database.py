"""Configuración de la base de datos y gestión de sesiones."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URl de la Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./featureflags.db")

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# Crear la clase SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear clase Base para modelos
Base = declarative_base()


def get_db():
    """
    Dependencia para obtener una sesión de base de datos.

    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa la base de datos y crea todas las tablas."""
    Base.metadata.create_all(bind=engine)
