from datetime import date

from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("/{hotel_id}", summary='Получение отеля по id')
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get("", summary='Получение списка всех отелей')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description='Адрес'),
        date_from: date = Query(example='2026-02-10'),
        date_to: date = Query(example='2026-02-15'),
):
    per_page = pagination.per_page or 5

    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )

    return await db.hotels.get_filtered_by_date(
        date_from=date_from,
        date_to=date_to,
    )


@router.post("", summary='Добавление нового отеля')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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

    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {'status': 'OK', "data": hotel}


@router.delete("/{hotel_id}", summary='Удаление отеля по id')
async def delete_hotel(db: DBDep, hotel_id: int):

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.put("/{hotel_id}", summary='Изменение всех данных отеля')
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary='Частичное изменение данных отеля')
async def part_edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):

    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}
