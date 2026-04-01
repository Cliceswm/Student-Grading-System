import sys
import os

from flask import app
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
    "TESTING": True,
    "WTF_CSRF_ENABLED": False
    })
    with app.test_client() as client:
        yield client


