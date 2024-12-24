import pytest
from httpx import AsyncClient
from app.main import app

# How to run tests:
# 1.) pytest tests/test_app.py
# 2.) poetry run pytest tests/test_app.py

@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI DynamoDB project!"}