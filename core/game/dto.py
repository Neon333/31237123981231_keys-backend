import datetime
from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    name: str


class UserImage(BaseModel):
    format: str
    base64_encoded_source: str


class Game(BaseModel):
    name: str
    description: str
    system_requirements: str
    current_price: int
    images: list[UserImage]
    key_category_id: int = None
    old_price: int = None
    genre_id_list: list[int] = []


class UserReview(BaseModel):
    id: int
    customer_name: str
    text: str
    rating: int
    date: datetime.date
    game_id: int
