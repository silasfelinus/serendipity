import pytest
from app.main import app

@pytest.mark.asyncio
async def test_home_route(client):
    response = await client.get('/')
    assert response.status_code == 200
    assert b"WonderWidget WonderLab" in await response.get_data()