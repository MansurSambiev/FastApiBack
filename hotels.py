from fastapi import Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 2, "title": "Москва", "name": "moscosmo"},
    {"id": 2, "title": "Краснодар", "name": "reddar"},
]


@router.get("", summary='Получение списка всех отелей')
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_




@router.post("", summary='Добавление нового отеля')
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
    return {'status': 'OK'}


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
