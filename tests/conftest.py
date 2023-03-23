import pytest
from quart.testing import QuartClient
from app.main import app

@pytest.fixture
def client():
    return QuartClient(app)
