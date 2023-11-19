import pytest
import os
from app import create_app
from app.models import db

SAMPLE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'amazing_company_2.pdf')

@pytest.fixture
def app():
    app = create_app('config.py')
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_file():
    with open(SAMPLE_FILE_PATH, 'rb') as file:
        return file.read()
    
@pytest.fixture
def clean_db(app):
    with app.app_context():
        db.create_all()  # Create database tables for testing
        yield db  # Provide the clean database to the tests
        db.drop_all()  # Drop tables after the test
