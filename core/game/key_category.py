from .models.key_category import KeyCategoryDataModel, KeyCategoryRepo


class KeyCategory:

    def __init__(self, db_instance: KeyCategoryDataModel):
        self._db_instance = db_instance

    @classmethod
    async def create(cls, name: str) -> 'KeyCategory':
        new_category = await KeyCategoryRepo.create(name)
        return cls.from_db_instance(new_category)

    @classmethod
    async def get_all(cls) -> list['KeyCategory']:
        return [cls.from_db_instance(category) for category in await KeyCategoryRepo.get_all()]

    @classmethod
    async def get_by_id(cls, category_id: int) -> 'KeyCategory':
        return cls.from_db_instance(await KeyCategoryRepo.get_category_by_id(category_id))

    @classmethod
    def from_db_instance(cls, db_instance: KeyCategoryDataModel) -> 'KeyCategory':
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
        return await self._db_instance.release_keys(count)

    async def append_keys(self, keys: list[str]):
        await self._db_instance.append_keys(keys)
