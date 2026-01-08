from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func
from src.repositories.hotels import HotelRepository
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


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
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.put("/{hotel_id}", summary='Изменение всех данных отеля')
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id))
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary='Частичное изменение данных отеля')
def part_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id))
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name

    return hotel
