from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description='Страница (начиная'),]
    per_page: Annotated[int | None, Query(3, ge=1, le=30, description='Количество отелей на страницу'),]


PaginationDep = Annotated[PaginationParams, Depends()]
