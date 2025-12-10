"""Main FastAPI application."""

from fastapi import FastAPI
from app.database import init_db
from app.routers.flags import router as flags_router
from app.middleware.error_handler import add_exception_handlers
import os

# Obtener el entorno actual
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
DEFAULT_FLAG_STRATEGY = os.getenv("DEFAULT_FLAG_STRATEGY", "permissive")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Crear FastAPI app
app = FastAPI(
    title="Feature Flag Hub",
    description="Sistema de gestión de feature flags con despliegue controlado",
    version="1.0.0",
)

# Inicializar base de datos
init_db()

# Agregar manejadores de excepciones
add_exception_handlers(app)

# Incluir routers
app.include_router(flags_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Feature Flag Hub API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "feature-flag-hub",
        "version": "1.0.0",
        # /health refleja el entorno
        "environment": ENVIRONMENT,
        "strategy": DEFAULT_FLAG_STRATEGY,
        "log_level": LOG_LEVEL,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
