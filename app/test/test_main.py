# app/test/test_main.py
import os
import pytest
from app.main import app
from app.gradio.interface import create_interface

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Serendipity" in response.data

def test_logger():
    from app.logging_config import setup_logging
    logger = setup_logging()
    assert logger is not None

def test_create_interface(mocker):
    # Mock Gradio's Library
    mocker.patch('app.gradio.interface.gr.Interface')

    # Call the create_interface function
    interface = create_interface()

    # Check if the interface is not None
    assert interface is not None