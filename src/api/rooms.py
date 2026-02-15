from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomPatch, RoomPatchRequest, RoomAdd, RoomAddRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("/{hotel_id}/rooms", summary='Получение свободных номеров по датам и id отеля')
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example='2026-02-10'),
        date_to: date = Query(example='2026-02-15'),
):
    return await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary='Получение номера по своему id и по id отеля')
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary='Добавление нового номера')
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(openapi_examples={
            '1': {'summary': 'Стандарт 1', 'value': {
                'title': 'Эконом 1 мест',
                'description': 'Стандартный одноместный номер',
                'price': 2000,
                'quantity': 10,
            }},
            '2': {'summary': 'Стандарт 2', 'value': {
                'title': 'Эконом 2 мест',
                'description': 'Стандартный двухместный номер',
                'price': 3000,
                'quantity': 7,
            }}
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.add(_room_data)
    await db.commit()

    return {'status': 'OK', "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменение всех данных номера')
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()

    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}", summary='Частичное изменение данных номера')
async def part_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удаление номера по id')
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {'status': 'OK'}
