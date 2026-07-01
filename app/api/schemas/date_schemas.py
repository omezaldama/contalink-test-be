from datetime import date

from pydantic import BaseModel


class DateRange(BaseModel):
    from_date: date
    to_date: date
