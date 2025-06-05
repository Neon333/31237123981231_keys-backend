from dataclasses import dataclass
from typing import Union

from sqlalchemy import update, func
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, Query

from .genre import GenreModel
from ...database import get_async_session
from ...database.sql_models import ReviewSqlModel
from ...database.sql_models.game import GameSqlModel, GenreSqlModel, GameGenrePivotTable
from ...utils.models import IgnoreUpdate
from ..dto import Game


@dataclass
class ImageInDB:
    filename: str


class GameInDB(Game):
    id: int
    visible: bool
    rating: int
    images: list[ImageInDB]
    genres: list


class GameRepoModel:

    @classmethod
    async def create(
        cls, name: str,
        description: str,
        system_requirements: str,
        current_price: int,
        genre_id_list: list[int],
        key_category_id: int = None,
        old_price: int = None,
    ) -> 'GameDataModel':
        async with get_async_session() as session:
            new_game = GameSqlModel(
                name=name,
                description=description,
                system_requirements=system_requirements,
                current_price=current_price,
                old_price=old_price,
                key_category_id=key_category_id,
            )
            new_game.genres = list(await session.scalars(select(GenreSqlModel).filter(GenreSqlModel.id.in_(genre_id_list))))

            session.add(new_game)
            await session.commit()
            await session.refresh(new_game)

            return GameDataModel.from_db_instance(new_game)

    @classmethod
    async def get_game_by(cls, game_id: int = None, alias: str = None, as_dto: bool = False) -> Union['GameDataModel', 'GameInDB']:
        field, value = (GameSqlModel.id, game_id) if game_id is not None else (GameSqlModel.alias, alias)
        async with get_async_session() as session:
            query = cls._create_game_fetch_query().filter(field == value)
            results = await session.execute(query)
            return cls._convert_results_queryset([results.first()], cls._get_obj_creator(dto=as_dto))[0]

    @classmethod
    async def get_games_total(cls, genre_id: int = None) -> int:
        async with get_async_session() as session:
            query = select(func.count(GameSqlModel.id)).filter(GameSqlModel.visible == True)
            if genre_id is not None:
                query = query.join(GameSqlModel.genres).filter(GenreSqlModel.id == genre_id)
            query_result = await session.execute(query)
            return query_result.scalar()

    @classmethod
    async def get_games(
        cls,
        count: int = None,
        offset: int = 0,
        name: str = None,
        genre_id: int = None,
        min_rating: int = None,
        only_visible: bool = True,
        as_dto: bool = False
    ) -> Union[list['GameInDB'], list['GameDataModel']]:
        """
        For games search
        """
        async with get_async_session() as session:
            query = cls._create_game_fetch_query().offset(offset)
            if count is not None:
                query = query.limit(count)
            if name is not None:
                query = query.filter(GameSqlModel.name.ilike(f'%{name}%'))
            if genre_id is not None:
                query = query.join(GameSqlModel.genres).filter(GenreSqlModel.id == genre_id)
            if only_visible:
                query = query.filter(
                    GameSqlModel.visible == True
                )

            games_fetched = await session.execute(query)

        results = cls._convert_results_queryset(games_fetched.unique(), cls._get_obj_creator(dto=as_dto))  # type:ignore
        if min_rating is not None:
            results = list(filter(lambda g: g.rating >= min_rating, results))

        results.sort(key=lambda g: g.rating, reverse=True)
        return results

    @classmethod
    def _convert_results_queryset(cls, queryset, obj_creator):
        games_converted = list()
        for game, rating in queryset:
            setattr(game, 'rating', rating)
            games_converted.append(game)

        return list(map(obj_creator, games_converted))

    @classmethod
    def _create_game_fetch_query(cls) -> Query:
        query = select(
            GameSqlModel,
            func.coalesce(func.avg(ReviewSqlModel.rating), 5).label('rating')
        ).join(
            ReviewSqlModel,
            GameSqlModel.id == ReviewSqlModel.game_id, isouter=True
        ).options(
            joinedload(GameSqlModel.images),
            joinedload(GameSqlModel.genres),
        ).group_by(
            GameSqlModel.id
        )

        return query

    @classmethod
    def _get_obj_creator(cls, dto: bool = False) -> callable:
        return GameDataModel.from_db_instance if not dto else lambda i: GameInDB(
            id=i.id,
            visible=i.visible,
            name=i.name,
            rating=i.rating,
            genres=[
                GenreModel(id=genre.id, name=genre.name)
                for genre in i.genres
            ],
            description=i.description,
            system_requirements=i.system_requirements,
            current_price=i.current_price,
            old_price=i.old_price,
            key_category_id=i.key_category_id,
            images=[
                ImageInDB(img.filename)
                for img in i.images
            ]
        )
    

class GameDataModel:

    def __init__(self, db_instance: GameSqlModel):
        self._db_instance = db_instance

    @classmethod
    def from_db_instance(cls, db_instance: GameSqlModel) -> 'GameDataModel':
        return cls(db_instance)

    @property
    def id(self) -> int:
        return self._db_instance.id

    @property
    def name(self) -> str:
        return self._db_instance.name

    @property
    def description(self) -> str:
        return self._db_instance.description

    @property
    def is_visible(self) -> bool:
        return self._db_instance.visible
    
    @property
    def system_requirements(self) -> str:
        return self._db_instance.system_requirements

    @property
    def current_price(self) -> int:
        return self._db_instance.current_price

    @property
    def old_price(self) -> int | None:
        return self._db_instance.old_price

    @property
    def rating(self) -> int:
        return int(self._db_instance.rating)

    async def set_visible(self, visible: bool):
        async with get_async_session() as session:
            db_instance_in_session: GameSqlModel = await session.get(GameSqlModel, self._db_instance.id)
            db_instance_in_session.visible = visible
            await session.commit()

    async def update(
        self, visible: bool = IgnoreUpdate,
        name: str = IgnoreUpdate,
        description: str = IgnoreUpdate,
        system_requirements: str = IgnoreUpdate,
        current_price: int = IgnoreUpdate,
        old_price: int = IgnoreUpdate,
        key_category_id: int = IgnoreUpdate,
    ):
        update_map = {
            'visible': visible,
            'name': name,
            'description': description,
            'system_requirements': system_requirements,
            'current_price': current_price,
            'old_price': old_price,
            'key_category_id': key_category_id
        }
        prepared_update_map = {
            k: v for k, v in update_map.items()
            if v != IgnoreUpdate
        }

        async with get_async_session() as session:
            query = (
                update(GameSqlModel)
                .where(GameSqlModel.id == self.id)
                .values(**prepared_update_map)
            )
            await session.execute(query)
            await session.commit()

    async def delete(self):
        async with get_async_session() as session:
            db_instance_in_session: GameSqlModel = await session.get(GameSqlModel, self._db_instance.id)
            await session.delete(db_instance_in_session)
            await session.commit()
