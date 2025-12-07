#!/bin/bash

# Script para generar archivos .env por entorno
# Uso: ./setup-env.sh

set -e

echo "Generando archivos de configuración por entorno..."

# Crear .env.dev
cat > .env.dev << 'EOF'
# Environment configuration - Development
ENVIRONMENT=dev
DEFAULT_FLAG_STRATEGY=permissive
DATABASE_URL=sqlite:///./data/featureflags_dev.db
API_VERSION=1.0.0
LOG_LEVEL=DEBUG
API_PORT=8000
EOF

echo "* .env.dev creado"

# Crear .env.staging
cat > .env.staging << 'EOF'
# Environment configuration - Staging
ENVIRONMENT=staging
DEFAULT_FLAG_STRATEGY=strict
DATABASE_URL=sqlite:///./data/featureflags_staging.db
API_VERSION=1.0.0
LOG_LEVEL=INFO
API_PORT=8001
EOF

echo "* .env.staging creado"

# Crear directorio data si no existe
if [ ! -d "data" ]; then
  mkdir -p data
  echo "* Directorio ./data/ creado"
fi

echo ""
echo "Configuración completada!"
echo ""
echo "Para ejecutar:"
echo "  Dev:     docker-compose -f docker-compose.dev.yml up --build"
echo "  Staging: docker-compose -f docker-compose.staging.yml up --build"
echo ""
echo "Health checks:"
echo "  Dev:     curl http://localhost:8000/health"
echo "  Staging: curl http://localhost:8001/health"
