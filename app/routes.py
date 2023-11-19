from datetime import datetime
from flask import Blueprint, render_template, current_app, request, jsonify, Response, abort
from app.errorHandlers import handle_generic_exception
from app.models import db, InvoiceExtraction
import requests
import base64

routes = Blueprint('routes', __name__)

@routes.route('/', methods=["GET"])
def index() -> Response:
    return render_template('index.html')

@routes.route("/process", methods=['POST'])
def process_data() -> Response:
    file = request.files['file']

    base64_data = base64.b64encode(file.read()).decode('utf-8')

    url = current_app.config["TYPLESS_URL"]
    auth_key = current_app.config["TYPLESS_API_KEY"]

    payload = {
        "file": base64_data,
        "file_name": file.filename,
        "document_type_name": "simple-invoice"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": auth_key
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response = response.json()

    # We want to have at least supplier name in the processed data
    extracted_fields = response['extracted_fields']
    supplier_name_dict = next((field for field in extracted_fields if field['name'] == 'supplier_name'), None)
    if supplier_name_dict:
        supplier_name_value = supplier_name_dict['values'][0]['value']
        if not supplier_name_value:
            abort(400, "Bad imput - supplier name couldn't be obtained.")
    else:
        abort (500, "Something wrong with Typless server!")

    return jsonify({
        'status': 'success',
        'message': 'Invoice processed successfully.',
        'data': response
    }), 200

@routes.route("/save", methods=['POST'])
def save_data() -> Response:
    data = request.json
    extracted_fields = data.get('extractedFields')

    # Convert date and float values
    supplier_name = extracted_fields['supplier_name'] if extracted_fields['supplier_name'] != "null" else None
    issue_date = datetime.strptime(extracted_fields['issue_date'], '%Y-%m-%d') if extracted_fields['issue_date'] != "null" else None
    pay_due_date = datetime.strptime(extracted_fields['pay_due_date'], '%Y-%m-%d') if extracted_fields['pay_due_date'] != "null" else None
    total_amount = float(extracted_fields['total_amount']) if extracted_fields['total_amount'] != "null" else None
    invoice_number = extracted_fields['invoice_number'] if extracted_fields['invoice_number'] != "null" else None

    # Save data to the database
    new_entry = InvoiceExtraction(
        supplier_name=supplier_name,
        issue_date=issue_date,
        pay_due_date=pay_due_date,
        total_amount=total_amount,
        invoice_number=invoice_number
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({
        'status': 'sucess',
        'message': 'Data saved successfully'}), 200
    