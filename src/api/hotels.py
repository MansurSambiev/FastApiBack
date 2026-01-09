from fastapi import Query, APIRouter, Body

from src.repositories.hotels import HotelRepository
from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("/{hotel_id}", summary='Получение отеля по id')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_one_or_none(id=hotel_id)


@router.get("", summary='Получение списка всех отелей')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description='Адрес'),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("", summary='Добавление нового отеля')
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'South resort',
        'location': 'Сочи, ул.Моря, 1'
    }},
    '2': {'summary': 'Дубай', 'value': {
        'title': 'Burge Khalifa',
        'location': 'Дубай, ул.Шейха, 2'
    }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', "data": hotel}


@router.delete("/{hotel_id}", summary='Удаление отеля по id')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.put("/{hotel_id}", summary='Изменение всех данных отеля')
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary='Частичное изменение данных отеля')
async def part_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
