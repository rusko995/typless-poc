import io
from datetime import datetime
from flask import Response
from werkzeug.datastructures import FileStorage
from app.models import InvoiceExtraction, db

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is the input for the Typless invoice processor' in response.data

def test_another_route(client):
    response: Response = client.get('/another')
    assert response.status_code == 404

def test_process_data(client):
    file_path = 'tests/files/amazing_company_2.pdf'

    # Simulate file upload in the request
    with open(file_path, 'rb') as file:
        file_storage = FileStorage(
            stream=io.BytesIO(file.read()),
            filename='tests/amazing_company_2.pdf',
            content_type='application/pdf'
        )

    payload = {'file': file_storage}
    response: Response = client.post('/process', data=payload)

    assert response.status_code == 200

def test_process_data_input_error(client):
    file_path = 'tests/files/empty_test.jpg'

    # Simulate file upload in the request
    with open(file_path, 'rb') as file:
        file_storage = FileStorage(
            stream=io.BytesIO(file.read()),
            filename='tests/empty_test.jpg',
            content_type='image/jpeg'
        )

    payload = {'file': file_storage}
    response: Response = client.post('/process', data=payload)

    assert response.status_code == 400

def test_process_data_wrong_token(client, monkeypatch):
    monkeypatch.setitem(client.application.config, 'TYPLESS_API_KEY', 'mocked_api_key')
    file_path = 'tests/files/empty_test.jpg'

    # Simulate file upload in the request
    with open(file_path, 'rb') as file:
        file_storage = FileStorage(
            stream=io.BytesIO(file.read()),
            filename='tests/empty_test.jpg',
            content_type='image/jpeg'
        )

    payload = {'file': file_storage}
    response: Response = client.post('/process', data=payload)

    assert response.status_code == 500

# TODO - clean testing state improvement
# If you want to have a clean state you can use also: def test_save_data(client, clean_db) and use clean_db instead of db
# In this case it would be recommended to have separate test_database.db (different config file would be needed)
def test_save_data(client):
    payload = {
        'extractedFields':{
            'supplier_name': 'Test Supplier',
            'issue_date': '2023-01-01',
            'pay_due_date': 'null',
            'total_amount': '350.0',
            'invoice_number': 'null'}
    }

    response = client.post('/save', json=payload)

    assert response.status_code == 200

    with db.session.begin():
        saved_entry = db.session.query(InvoiceExtraction).order_by(InvoiceExtraction.id.desc()).first()
        assert saved_entry is not None
        assert saved_entry.supplier_name == 'Test Supplier'
        assert saved_entry.issue_date == datetime.strptime('2023-01-01', '%Y-%m-%d').date()
        assert saved_entry.invoice_number == None

# Missing other fields --> error
def test_save_data_error(client):
    payload = {
        'extractedFields':{
            'supplier_name': 'Test'
        }
    }
    response = client.post('/save', json=payload)

    assert response.status_code == 500