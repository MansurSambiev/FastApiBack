from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomRepository
from src.schemas.rooms import RoomPatch, RoomPatchRequest, RoomAdd, RoomAddRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("/{hotel_id}/rooms", summary='Получение всех номеров по id отеля')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary='Получение номера по своему id и по id отеля')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms/", summary='Добавление нового номера')
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    '1': {'summary': 'Стандарт 1', 'value': {
        'title': 'Эконом 1 мест',
        'description': 'Стандартный одноместный номер',
        'price': '2000',
        'quantity': '10',
    }},
    '2': {'summary': 'Стандарт 2', 'value': {
        'title': 'Эконом 2 мест',
        'description': 'Стандартный двухместный номер',
        'price': '3000',
        'quantity': '7',
    }}
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomRepository(session).add(_room_data)
        await session.commit()

    return {'status': 'OK', "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменение всех данных номера')
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomRepository(session).edit(_room_data, id=room_id)
        await session.commit()

    return {'status': 'OK'}


@router.patch("/{hotel_id}/rooms/{room_id}", summary='Частичное изменение данных номера')
async def part_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomRepository(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'status': 'OK'}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удаление номера по id')
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'status': 'OK'}
