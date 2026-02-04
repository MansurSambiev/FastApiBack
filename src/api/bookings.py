from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('', summary='Добавление бронирования')
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {'status': 'OK', 'data': booking}


@router.get('', summary='Получение всех бронирований')
async def get_booking(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get('/me', summary='Получение моих бронировваний')
async def get_my_booking(
        db: DBDep,
        user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)
