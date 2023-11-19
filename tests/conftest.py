import pytest
import os
from app import create_app
from app.models import db

@pytest.fixture
def app():
    app = create_app('config.py')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
    
# @pytest.fixture
# def clean_db(app):
#     with app.app_context():
#         db.create_all()  # Create database tables for testing
#         yield db  # Provide the clean database to the tests
#         db.drop_all()  # Drop tables after the test
