"""Main FastAPI application."""

from fastapi import FastAPI
from app.database import init_db
from app.routers.flags import router as flags_router
from app.middleware.error_handler import add_exception_handlers

# Crear FastAPI app
app = FastAPI(
    title="Feature Flag Hub",
    description="Sistema de gestión de feature flags con despliegue controlado",
    version="1.0.0"
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
    return {
        "message": "Feature Flag Hub API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "feature-flag-hub",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)