import os.path
from sqlalchemy.future import select
from ...database.sql_models.game import PreviewImageSqlModel
from ...database import get_async_session


class PreviewImageRepo:

    @classmethod
    async def create_image(cls, path: str, filename: str, game_id: int) -> 'PreviewImageDataModel':
        async with get_async_session() as session:
            new_image = PreviewImageSqlModel(
                path=path,
                filename=filename,
                game_id=game_id
            )
            session.add(new_image)
            await session.commit()
            await session.refresh(new_image)

            return PreviewImageDataModel.from_db_instance(new_image)

    @classmethod
    async def get_images_by_game_id(cls, game_id: int) -> list['PreviewImageDataModel']:
        async with get_async_session() as session:
            fetched_reviews = await session.scalars(select(PreviewImageSqlModel).where(PreviewImageSqlModel.game_id == game_id))
            return [
                PreviewImageDataModel.from_db_instance(db_instance)
                for db_instance in fetched_reviews.all()
            ]


class PreviewImageDataModel:

    def __init__(self, db_instance: PreviewImageSqlModel):
        self._db_instance = db_instance

    @classmethod
    def from_db_instance(cls, db_instance: PreviewImageSqlModel) -> 'PreviewImageDataModel':
        return cls(db_instance)

    @property
    def id(self) -> int:
        return self._db_instance.id

    @property
    def path(self) -> str | os.PathLike:
        return self._db_instance.path

    @property
    def filename(self) -> str | os.PathLike:
        return self._db_instance.filename

    async def delete(self):
        async with get_async_session() as session:
            db_instance_in_session = await session.get(PreviewImageSqlModel, self._db_instance.id)
            await session.delete(db_instance_in_session)
            await session.commit()
