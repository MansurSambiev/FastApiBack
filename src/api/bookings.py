from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('', summary='Добавление бронирования')
async def create_booking(db: DBDep, booking_data: BookingAdd):

    booking = await db.bookings.add(booking_data)
    await db.commit()

    return {'status': 'OK', 'data': booking}
