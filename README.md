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

