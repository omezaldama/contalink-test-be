from datetime import date, datetime, time
import json
from typing import List

from sqlalchemy.orm import Session

from app.api.schemas.invoice_schemas import InvoiceSchema
from app.models.invoice import Invoice
from app.services.cache_service import CacheService


class InvoicesService:
    def __init__(self, session: Session):
        self._cache = CacheService()
        self._session = session

    def get_by_date_range(self, from_date: date, to_date: date) -> List[InvoiceSchema]:
        cache_key = f'{from_date}_{to_date}'
        cached_invoices = self._cache.get(cache_key)

        if cached_invoices:
            return json.loads(cached_invoices)

        db_invoices = self._session.query(Invoice) \
            .where(Invoice.invoice_date.between(
                from_date, datetime.combine(to_date, time.max),
            )) \
            .all()
        invoices = [
            InvoiceSchema.model_validate(invoice).model_dump()
            for invoice in db_invoices
        ]

        self._cache.set(
            cache_key,
            json.dumps(invoices, default=str)
        )
        return invoices
