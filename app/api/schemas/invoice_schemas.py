from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class InvoiceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_number: str
    total: float
    invoice_date: datetime
    status: str
    active: bool


class GetInvoicesResponse(BaseModel):
    invoices: List[InvoiceSchema]
