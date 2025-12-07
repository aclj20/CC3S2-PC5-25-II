# CC3S2-PC5-25-II

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Configurar variables de entorno:
```bash
cp .env.example .env
```

Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## Ejecutar con Docker Compose (Sprint 2)

### Setup Inicial

Generar archivos de configuración por entorno:
```bash
./setup-env.sh
```

Esto crea:
- `.env.dev` - Configuración para desarrollo
- `.env.staging` - Configuración para staging
- `./data/` - Directorio para bases de datos

### Entorno de desarrollo
```bash
docker-compose -f docker-compose.dev.yml up --build
```
- Usa `.env.dev` (ENVIRONMENT=dev, LOG_LEVEL=DEBUG)
- Ejecuta en puerto 8000
- Base de datos: `./data/featureflags_dev.db`

### Entorno de staging (producción-like)
```bash
docker-compose -f docker-compose.staging.yml up --build
```
- Usa `.env.staging` (ENVIRONMENT=staging, LOG_LEVEL=INFO)
- Ejecuta en puerto 8001
- Base de datos: `./data/featureflags_staging.db`
- Imagen endurecida con usuario no-root

### Health checks
```bash
curl http://localhost:8000/health  # dev
curl http://localhost:8001/health  # staging
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "feature-flag-hub",
  "version": "1.0.0",
  "environment": "dev",
  "strategy": "permissive",
  "log_level": "DEBUG"
}
  "version": "1.0.0",
  "environment": "dev",
  "strategy": "permissive",
  "log_level": "DEBUG"
}
```

## Endpoints Disponibles

### Flags

- `GET /api/flags` - Listar todos los flags
- `POST /api/flags` - Crear un nuevo flag
- `GET /api/flags/{name}` - Obtener un flag específico
- `PUT /api/flags/{name}` - Actualizar un flag
- `GET /api/flags/evaluate` - Evaluar un flag para un usuario específico

### Crear un flag:
```bash
curl -X POST http://localhost:8000/api/flags \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new-feature",
    "description": "Nueva funcionalidad",
    "enabled": true,
    "rollout_percentage": 50,
    "allowed_users": ["user1", "user2"]
  }'
```

### Listar flags:
```bash
curl http://localhost:8000/api/flags
```

### Obtener un flag:
```bash
curl http://localhost:8000/api/flags/new-feature
```

### Actualizar un flag:
```bash
curl -X PUT http://localhost:8000/api/flags/new-feature \
  -H "Content-Type: application/json" \
  -d '{
    "rollout_percentage": 75
  }'
```

### Evaluar un flag para un usuario:
```bash
curl "http://localhost:8000/api/flags/evaluate?user_id=user123&flag=new-feature"
```

**Respuesta:**
```json
{
  "flag_name": "new-feature",
  "enabled": true,
  "reason": "user_in_allowlist"
}
```

## Evaluación de Feature Flags

El endpoint `/api/flags/evaluate` implementa reglas de segmentación para determinar si un usuario debe recibir una feature:

### Reglas de Segmentación (en orden de prioridad):

1. **Flag deshabilitada**: Si `enabled = false`, todos los usuarios son denegados
   - Razón: `"flag_disabled"`

2. **Allowlist de usuarios**: Usuarios en `allowed_users` siempre reciben la feature
   - Razón: `"user_in_allowlist"`

3. **Rollout por porcentaje**: Distribución determinística basada en hash
   - Usa `SHA-256(user_id:flag_name)` para consistencia
   - El mismo usuario siempre obtiene el mismo resultado
   - Razón: `"rollout_percentage"` o `"not_in_rollout_percentage"`

4. **Denegación por defecto**: Si está habilitada pero sin rollout ni allowlist
   - Razón: `"default_deny"`

### Ejemplos de Uso

**Usuario en allowlist:**
```bash
curl "http://localhost:8000/api/flags/evaluate?user_id=user1&flag=new-feature"
# Respuesta: {"flag_name": "new-feature", "enabled": true, "reason": "user_in_allowlist"}
```

**Rollout al 50%:**
```bash
# El resultado depende del hash del usuario
curl "http://localhost:8000/api/flags/evaluate?user_id=user456&flag=new-feature"
# Respuesta: {"flag_name": "new-feature", "enabled": true/false, "reason": "rollout_percentage" o "not_in_rollout_percentage"}
```

**Flag deshabilitada:**
```bash
curl "http://localhost:8000/api/flags/evaluate?user_id=user789&flag=disabled-feature"
# Respuesta: {"flag_name": "disabled-feature", "enabled": false, "reason": "flag_disabled"}
```

## Estructura del Proyecto
```
featureflags/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── schemas/         # Schemas Pydantic
│   ├── routers/         # Endpoints REST
│   ├── services/        # Lógica de negocio (evaluación de flags)
│   ├── validators/      # Validadores de datos
│   ├── middleware/      # Middleware y error handlers
│   ├── database.py      # Configuración de BD
│   ├── exceptions.py    # Excepciones personalizadas
│   └── main.py          # Aplicación principal
├── requirements.txt
└── README.md
```

## Testing y Validación Automática (Sprint 1)

Este proyecto incluye una suite completa de pruebas unitarias y un pipeline de integración continua para garantizar la calidad del código desde el primer sprint.

### **Ejecución de Tests Localmente**

Para correr todos los tests:

```bash
pytest -vv
```

Los tests usan una base de datos SQLite aislada (`test_featureflags.db`) configurada mediante `conftest.py`, por lo que no afectan los datos reales del proyecto.

### **Contenido Principal de los Tests**

Los tests cubren:

* **/health**

  * Verifica estado y metadatos del servicio

* **CRUD de flags (`/api/flags`)**

  * Crear, listar, obtener y actualizar flags
  * Validación de esquemas `FlagResponse` y `FlagListResponse`
  * Manejo correcto de errores (`FlagNotFoundException → 404`)

* **Evaluación de flags (`/api/flags/evaluate`)**

  * Flag deshabilitada
  * Usuario en allowlist
  * Rollout determinístico
  * Caso default deny
  * Validación del esquema `EvaluateResponse`

### **Estructura de pruebas**

```
tests/
├── conftest.py          # DB de pruebas + TestClient configurado
├── test_health.py       # Endpoint /health
├── test_flags_crud.py   # CRUD de flags
└── test_evaluate.py     # Lógica de segmentación y evaluación
```

---

## Pipeline CI (Integración Continua)

El proyecto cuenta con un workflow automatizado que corre en cada push y pull request:

**Ruta:**
`.github/workflows/ci.yml`

### **Validaciones automáticas incluidas:**

* Formato con `black --check .`
* Análisis estático con `ruff check .`
* Ejecución completa de la suite de tests con `pytest -vv`

Esto garantiza:

* Código consistentemente formateado
* Detección temprana de errores
* Validación continua de endpoints críticos
* Verificación del comportamiento de la API en cada cambio relevante

Para reproducir localmente lo mismo que hace el CI:

```bash
black --check .
ruff check .
pytest -vv
```
