from sqlalchemy.future import select
from ...database.sql_models.key.category import KeyCategorySqlModel, SteamKeySqlModel
from ...database import get_async_session


class KeyCategoryRepo:

    @classmethod
    async def create(cls, name: str) -> 'KeyCategoryDataModel':
        async with get_async_session() as session:
            new_category = KeyCategorySqlModel(name=name)
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)

            return KeyCategoryDataModel.from_db_instance(new_category)

    @classmethod
    async def get_category_by_id(cls, category_id: int) -> 'KeyCategoryDataModel':
        async with get_async_session() as session:
            category = await session.get(KeyCategorySqlModel, category_id)
            return KeyCategoryDataModel.from_db_instance(category)

    @classmethod
    async def get_all(cls) -> list['KeyCategoryDataModel']:
        async with get_async_session() as session:
            query_result = await session.execute(select(KeyCategorySqlModel))
            categories = query_result.scalars()
            return [KeyCategoryDataModel.from_db_instance(category) for category in categories]


class KeyCategoryDataModel:

    def __init__(self, db_instance: KeyCategorySqlModel):
        self._db_instance = db_instance

    @classmethod
    def from_db_instance(cls, db_instance: KeyCategorySqlModel) -> 'KeyCategoryDataModel':
        return cls(db_instance)

    @property
    def id(self) -> int:
        return self._db_instance.id

    @property
    def name(self) -> str:
        return self._db_instance.name

    @property
    def count_keys(self) -> int:
        return self._db_instance.count_keys

    async def release_keys(self, count: int = 1) -> list[str]:
        async with get_async_session() as session:
            query = select(SteamKeySqlModel).where(SteamKeySqlModel.category_id == self.id).limit(count).with_for_update()
            query_result = await session.execute(query)
            return [key.value for key in query_result.scalars()]

    async def append_keys(self, keys: list[str]):
        async with get_async_session() as session:
            session.add_all([SteamKeySqlModel(value=key, category_id=self.id) for key in keys])
            await session.commit()
