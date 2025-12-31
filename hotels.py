from fastapi import Query, APIRouter, Body
from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 8, "title": "Москва", "name": "moscosmo"},
    {"id": 9, "title": "Краснодар", "name": "reddar"},
]


@router.get("", summary='Получение списка всех отелей')
def get_hotels(
        pagination: PaginationDep,
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

    # total = len(hotels_)
    # start = (page - 1) * per_page
    # end = start + per_page
    #
    # if not hotels_ and page > 1:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f'Страница {page} не найдена. Общее число страниц {total - 1 // per_page + 1}'
    #     )
    #
    # return hotels_[start:end]

    return hotels_[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]


@router.post("", summary='Добавление нового отеля')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Отель Сочи у моря',
        'name': 'sochi_u_morya'
    }},
    '2': {'summary': 'Дубай', 'value': {
        'title': 'Отель Дубай у фонтана',
        'name': 'dubai_fountain'
    }}
})
):
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
