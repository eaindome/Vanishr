import pytest
from httpx import AsyncClient
from app.main import app

USER = {
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "address": "123 Test St",
}

BROKER = {
    "name": "Test Broker",
    "opt_out_method": "email",
    "url": "http://broker.com",
    "notes": "Test notes",
}


@pytest.mark.asyncio
async def test_create_and_get_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create user
        resp = await ac.post("/users/", auth=("admin", "changeme"), json=USER)
        assert resp.status_code == 200
        user = resp.json()
        assert user["email"] == USER["email"]
        user_id = user["id"]
        # Get user
        resp = await ac.get(f"/users/{user_id}", auth=("admin", "changeme"))
        assert resp.status_code == 200
        assert resp.json()["id"] == user_id


@pytest.mark.asyncio
async def test_list_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/users/", auth=("admin", "changeme"))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_create_and_list_broker():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create broker
        resp = await ac.post("/brokers/", auth=("admin", "changeme"), json=BROKER)
        assert resp.status_code == 200
        broker = resp.json()
        assert broker["name"] == BROKER["name"]
        # List brokers
        resp = await ac.get("/brokers/", auth=("admin", "changeme"))
        assert resp.status_code == 200
        brokers = resp.json()
        assert any(b["name"] == BROKER["name"] for b in brokers)


@pytest.mark.asyncio
async def test_create_and_list_request():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create user and broker first
        user_resp = await ac.post("/users/", auth=("admin", "changeme"), json=USER)
        broker_resp = await ac.post(
            "/brokers/", auth=("admin", "changeme"), json=BROKER
        )
        user_id = user_resp.json()["id"]
        broker_id = broker_resp.json()["id"]
        # Create request
        req_payload = {"user_id": user_id, "broker_id": broker_id}
        resp = await ac.post("/requests/", auth=("admin", "changeme"), json=req_payload)
        assert resp.status_code == 200
        req = resp.json()
        assert req["user_id"] == user_id
        # List requests
        resp = await ac.get("/requests/", auth=("admin", "changeme"))
        assert resp.status_code == 200
        requests = resp.json()
        assert any(r["user_id"] == user_id for r in requests)


@pytest.mark.asyncio
async def test_auth_required():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/users/")
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_user_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/users/999999", auth=("admin", "changeme"))
        assert resp.status_code == 404
