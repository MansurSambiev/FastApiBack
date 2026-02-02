from datetime import date

from pydantic import BaseModel


class BookingAdd(BaseModel):
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id: int


class BookingPatch(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
