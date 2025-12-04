from http import HTTPStatus


def _create_flag(client, payload: dict) -> None:
    response = client.post("/api/flags", json=payload)
    assert response.status_code == HTTPStatus.CREATED


def test_evaluate_returns_disabled_when_flag_is_disabled(client):
    payload = {
        "name": "disabled-feature",
        "description": "Feature deshabilitada",
        "enabled": False,
        "rollout_percentage": 100,
        "allowed_users": ["user-123"],
    }
    _create_flag(client, payload)

    resp = client.get(
        "/api/flags/evaluate",
        params={"user_id": "user-123", "flag": "disabled-feature"},
    )
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert data["flag_name"] == "disabled-feature"
    assert data["enabled"] is False
    assert data["reason"] == "flag_disabled"


def test_evaluate_returns_enabled_for_user_in_allowlist(client):
    payload = {
        "name": "beta-dashboard",
        "description": "Dashboard beta",
        "enabled": True,
        "rollout_percentage": 0,
        "allowed_users": ["user-123"],
    }
    _create_flag(client, payload)

    resp = client.get(
        "/api/flags/evaluate",
        params={"user_id": "user-123", "flag": "beta-dashboard"},
    )
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert data["flag_name"] == "beta-dashboard"
    assert data["enabled"] is True
    assert data["reason"] == "user_in_allowlist"


def test_evaluate_returns_enabled_when_rollout_is_100(client):
    payload = {
        "name": "full-rollout-feature",
        "description": "Feature con rollout 100%",
        "enabled": True,
        "rollout_percentage": 100,
        "allowed_users": [],
    }
    _create_flag(client, payload)

    resp = client.get(
        "/api/flags/evaluate",
        params={"user_id": "random-user", "flag": "full-rollout-feature"},
    )
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert data["flag_name"] == "full-rollout-feature"
    assert data["enabled"] is True
    assert data["reason"] == "rollout_percentage"


def test_evaluate_returns_default_deny_when_not_in_allowlist_and_no_rollout(client):
    payload = {
        "name": "strict-feature",
        "description": "Feature sin allowlist ni rollout",
        "enabled": True,
        "rollout_percentage": 0,
        "allowed_users": [],
    }
    _create_flag(client, payload)

    resp = client.get(
        "/api/flags/evaluate",
        params={"user_id": "some-user", "flag": "strict-feature"},
    )
    assert resp.status_code == HTTPStatus.OK

    data = resp.json()
    assert data["flag_name"] == "strict-feature"
    assert data["enabled"] is False
    assert data["reason"] == "default_deny"
