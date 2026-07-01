import resend
from sqlalchemy import func, select

from app.config import settings
from app.db.session import SessionLocal
from app.models.invoice import Invoice
from app.util.email_templates import top_days_email_template


resend.api_key = settings.resend_api_key


class TopSalesDaysNotificationService:
    def __init__(self):
        self._session = SessionLocal()

    def _get_top_days_list(self):
        invoice_day = func.date_trunc("day", Invoice.invoice_date).label("invoice_day")
        stmt = (
            select(
                invoice_day,
                func.sum(Invoice.total).label("total_sales"),
            )
            .group_by(invoice_day)
            .order_by(func.sum(Invoice.total).desc())
            .limit(10)
        )
        return self._session.execute(stmt).all()

    def _create_email_html(self, days_list) -> str:
        list_items = '\n'.join([
            f'<li><b>{day.invoice_day.strftime("%Y-%m-%d")}</b>: {day.total_sales}</li>'
            for day in days_list
        ])
        return top_days_email_template.substitute(list_items=list_items)

    def _send_email(self, content: str) -> None:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": settings.email_receiver,
            "subject": "Top sales days daily report",
            "html": content,
        })

    def send_top_days_email(self):
        days_list = self._get_top_days_list()
        html_content = self._create_email_html(days_list)
        self._send_email(html_content)
