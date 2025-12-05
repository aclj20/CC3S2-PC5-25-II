from http import HTTPStatus


def test_create_flag_and_get_by_name(client):
    payload = {
        "name": "New-Homepage",  # se normaliza a minúsculas por FlagBase
        "description": "Nueva homepage para pruebas",
        "enabled": True,
        "rollout_percentage": 50,
        "allowed_users": ["user1", "user2"],
    }

    # Crear flag
    create_resp = client.post("/api/flags", json=payload)
    assert create_resp.status_code == HTTPStatus.CREATED

    created = create_resp.json()
    # Pydantic normaliza name a minúsculas
    assert created["name"] == "new-homepage"
    assert created["description"] == "Nueva homepage para pruebas"
    assert created["enabled"] is True
    assert created["rollout_percentage"] == 50
    assert created["allowed_users"] == ["user1", "user2"]
    # FlagResponse añade id y created_at
    assert isinstance(created["id"], int)
    assert "created_at" in created

    # Obtener flag por nombre
    get_resp = client.get("/api/flags/new-homepage")
    assert get_resp.status_code == HTTPStatus.OK

    data = get_resp.json()
    assert data["name"] == "new-homepage"
    assert data["description"] == "Nueva homepage para pruebas"
    assert data["enabled"] is True
    assert data["rollout_percentage"] == 50
    assert data["allowed_users"] == ["user1", "user2"]
    assert isinstance(data["id"], int)
    assert "created_at" in data


def test_list_flags_returns_collection_and_total(client):
    resp = client.get("/api/flags")
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert "flags" in data
    assert "total" in data
    assert isinstance(data["flags"], list)
    assert isinstance(data["total"], int)

    # Cada item debe cumplir esquema de FlagResponse
    if data["flags"]:
        flag = data["flags"][0]
        assert "id" in flag
        assert "name" in flag
        assert "enabled" in flag
        assert "created_at" in flag


def test_update_flag_changes_fields(client):
    # Crear flag inicial
    initial_payload = {
        "name": "beta-feature",
        "description": "Feature beta inicial",
        "enabled": True,
        "rollout_percentage": 10,
        "allowed_users": [],
    }
    client.post("/api/flags", json=initial_payload)

    # Actualizar
    update_payload = {
        "description": "Feature beta actualizada",
        "enabled": False,
        "rollout_percentage": 80,
        "allowed_users": ["vip-user"],
    }

    update_resp = client.put("/api/flags/beta-feature", json=update_payload)
    assert update_resp.status_code == HTTPStatus.OK

    data = update_resp.json()
    assert data["name"] == "beta-feature"
    assert data["description"] == "Feature beta actualizada"
    assert data["enabled"] is False
    assert data["rollout_percentage"] == 80
    assert data["allowed_users"] == ["vip-user"]


def test_get_flag_not_found_returns_404_with_error_payload(client):
    resp = client.get("/api/flags/non-existent-flag")
    assert resp.status_code == HTTPStatus.NOT_FOUND

    data = resp.json()
    # manejador de FlagNotFoundException en error_handler
    assert data["error"] == "Flag no encontrada"
    assert data["flag_name"] == "non-existent-flag"
    assert "message" in data
