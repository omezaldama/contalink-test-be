from datetime import datetime, timedelta
import json

from fastapi.testclient import TestClient
from pytest import Session

from app.main import app
from app.models.invoice import Invoice
from app.tests.conftest import TestSessionLocal, test_db


client = TestClient(app)


def insert_invoice(session: Session, **kwargs):
    invoice_data = {
        'id': 1,
        'invoice_number': 'abc123',
        'total': 100,
        'invoice_date': datetime.now(),
        'status': 'ok',
        'active': True,
    }
    invoice_data.update(kwargs)

    invoice = Invoice(**invoice_data)
    session.add(invoice)
    session.commit()
    session.refresh(invoice)


def test_get_invoices(test_db):
    session = TestSessionLocal()

    invoice_date = datetime.now()
    invoice_number = 'INV2026'
    insert_invoice(session, invoice_date=invoice_date, invoice_number=invoice_number)

    response = client.get(
        f'api/invoices?from_date={invoice_date.strftime('%Y-%m-%d')}&to_date={invoice_date.strftime('%Y-%m-%d')}',
    )
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert len(content['invoices']) == 1
    assert content['invoices'][0]['invoice_number'] == invoice_number

    response = client.get(
        f'api/invoices?from_date={(
            invoice_date - timedelta(days=2)
        ).strftime('%Y-%m-%d')}&to_date={(
            invoice_date - timedelta(days=1)
        ).strftime('%Y-%m-%d')}',
    )
    content = json.loads(response.content.decode('utf-8'))
    assert len(content['invoices']) == 0
