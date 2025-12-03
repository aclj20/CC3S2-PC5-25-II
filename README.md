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

## Estructura del Proyecto
```
featureflags/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── schemas/         # Schemas Pydantic
│   ├── routers/         # Endpoints REST
│   ├── validators/      # Validadores de datos
│   ├── middleware/      # Middleware y error handlers
│   ├── database.py      # Configuración de BD
│   ├── exceptions.py    # Excepciones personalizadas
│   └── main.py          # Aplicación principal
├── requirements.txt
└── README.md
```

