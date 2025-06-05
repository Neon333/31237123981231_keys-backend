import datetime
from sqlalchemy.future import select
from ...database.sql_models.game import ReviewSqlModel
from ...database import get_async_session
from ..dto import UserReview


class ReviewRepo:

    @classmethod
    async def create(cls, game_id: int, text: str, rating: int, customer_name: str, date: datetime.date) -> 'ReviewDataModel':
        async with get_async_session() as session:
            new_game = ReviewSqlModel(
                customer_name=customer_name,
                text=text,
                rating=rating,
                date=date,
                game_id=game_id
            )
            session.add(new_game)
            await session.commit()
            await session.refresh(new_game)

            return ReviewDataModel.from_db_instance(new_game)
    
    @classmethod
    async def get_review_by_id(cls, review_id: int) -> 'ReviewDataModel':
        async with get_async_session() as session:
            return ReviewDataModel.from_db_instance(await session.get(ReviewSqlModel, review_id))

    @classmethod
    async def get_reviews_by_game_id(cls, game_id: int, as_dto: bool = False) -> list['ReviewDataModel']:
        async with get_async_session() as session:
            fetched_reviews = await session.scalars(select(ReviewSqlModel).where(ReviewSqlModel.game_id == game_id))
            return [
                cls._get_obj_creator(dto=as_dto)(db_instance)
                for db_instance in fetched_reviews.all()
            ]

    @classmethod
    def _get_obj_creator(cls, dto: bool = False) -> callable:
        return ReviewDataModel.from_db_instance if not dto else lambda i: UserReview(
            id=i.id,
            customer_name=i.customer_name,
            rating=i.rating,
            text=i.text,
            date=i.date,
            game_id=i.game_id
        )


class ReviewDataModel:

    def __init__(self, db_instance: ReviewSqlModel):
        self._db_instance = db_instance

    @classmethod
    def from_db_instance(cls, db_instance: ReviewSqlModel) -> 'ReviewDataModel':
        return cls(db_instance)

    @property
    def id(self) -> int:
        return self._db_instance.id

    @property
    def game_id(self) -> int:
        return self._db_instance.game_id

    @property
    def rating(self) -> int:
        return self._db_instance.rating

    @property
    def text(self) -> str:
        return self._db_instance.text

    @property
    def customer_name(self) -> str:
        return self._db_instance.customer_name

    @property
    def date(self) -> datetime.date:
        return self._db_instance.date

    async def delete(self):
        async with get_async_session() as session:
            db_instance_in_session: ReviewSqlModel = await session.get(ReviewSqlModel, self._db_instance.id)
            await session.delete(db_instance_in_session)
            await session.commit()
