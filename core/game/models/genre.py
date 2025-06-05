from dataclasses import dataclass
from sqlalchemy.future import select
from ...database import get_async_session
from ...database.sql_models.game import GenreSqlModel


@dataclass
class GenreModel:
    id: int
    name: str


class GenreRepo:

    @classmethod
    async def get_all(cls) -> list[GenreModel]:
        async with get_async_session() as session:
            query_result = await session.scalars(select(GenreSqlModel))
            t = [GenreModel(id=g.id, name=g.name) for g in query_result]
            return t

    @classmethod
    async def create(cls, name: str):
        async with get_async_session() as session:
            session.add(GenreSqlModel(name=name))
            await session.commit()
