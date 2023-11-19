from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class InvoiceExtraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(255))
    issue_date = db.Column(db.Date, nullable=True)
    pay_due_date = db.Column(db.Date, nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    invoice_number = db.Column(db.String(50), nullable=True) 
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
