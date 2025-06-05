import datetime

from pydantic import Field, BaseModel
from core.game.dto import Game, UserImage, UserReview


class GameCreateSchema(Game):
    pass


class EditGameSchema(BaseModel):
    visible: bool | None = None
    name: str | None = None
    description: str | None = None
    system_requirements: str | None = None
    current_price: int | None = None
    key_category_id: int | None = None
    old_price: int | None = None
    new_images: list[UserImage] = Field(default_factory=lambda: [])
    drop_images: list[str] = Field(default_factory=lambda: [])


class UserReviewCreateSchema(BaseModel):
    customer_name: str
    text: str
    rating: int
    date: datetime.date
    game_id: int


class ReviewInAdminPanel(BaseModel):
    id: int
    game_id: int
    customer_name: str
    text: str
    rating: int
    date: datetime.date
