from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.schemas.date_schemas import DateRange
from app.api.schemas.invoice_schemas import GetInvoicesResponse
from app.db.session import get_session
from app.services.get_invoices_service import InvoicesService


router = APIRouter(prefix='/api')

@router.get(
    '/invoices',
    response_model=GetInvoicesResponse,
    status_code=status.HTTP_200_OK
)
def get_invoices(
    *,
    session: Session = Depends(get_session),
    date_range: DateRange,
):
    invoices = InvoicesService(session).get_by_date_range(date_range.from_date, date_range.to_date)
    return {'invoices': invoices}
