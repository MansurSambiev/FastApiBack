from datetime import date

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    User_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int
