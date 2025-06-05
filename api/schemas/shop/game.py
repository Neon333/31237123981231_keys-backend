from pydantic import BaseModel

from core.game.dto import Genre
from core.game.models.game import ImageInDB


class GameOnSale(BaseModel):
    id: int
    name: str
    description: str
    system_requirements: str
    current_price: int
    old_price: int | None
    rating: int
    images: list[ImageInDB]
    genres: list[Genre]
