from pydantic import BaseModel


class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPATCH(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
