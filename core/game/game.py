import datetime
from base64 import b64decode
from io import BytesIO

from .dto import UserImage
from .models.game import GameRepoModel, GameDataModel
from .models.preview_image import PreviewImageRepo, PreviewImageDataModel
from .models.review import ReviewRepo, ReviewDataModel
from ..hosting import get_image_hosting
from uuid import uuid4


class GameReview:

    def __init__(self, db_instance: ReviewDataModel):
        self._db_instance = db_instance

    @property
    def id(self) -> int:
        return self._db_instance.id

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

    @classmethod
    async def create(cls, game_id: int, text: str, rating: int, customer_name: str, date: datetime.date) -> 'GameReview':
        return cls.from_db_instance(await ReviewRepo.create(game_id, text, rating, customer_name, date))

    @classmethod
    def from_db_instance(cls, db_instance: ReviewDataModel) -> 'GameReview':
        return cls(db_instance)


class GamePreviewImage:

    def __init__(self, db_instance: PreviewImageDataModel):
        self._db_instance = db_instance

    @property
    def id(self) -> int:
        return self._db_instance.id

    @property
    def path(self) -> str:
        return self._db_instance.path

    @property
    def filename(self) -> str:
        return self._db_instance.filename

    @classmethod
    async def create(cls, game_id: int, image_bytes: bytes | BytesIO, filename: str) -> 'GamePreviewImage':
        image_file_data = await get_image_hosting().store_image(image_bytes, filename)
        image_in_db = await PreviewImageRepo.create_image(
            image_file_data.path, image_file_data.filename, game_id
        )
        return cls.from_db_instance(image_in_db)

    @classmethod
    def from_db_instance(cls, db_instance: PreviewImageDataModel) -> 'GamePreviewImage':
        return cls(db_instance)

    async def delete(self):
        await self._db_instance.delete()
        await get_image_hosting().drop_image(self.filename)


class Game:

    def __init__(self, db_instance: GameDataModel):
        self._db_instance = db_instance

    @classmethod
    async def create(
        cls, name: str,
        description: str,
        system_requirements: str,
        current_price: int,
        genre_id_list: list[int],
        images: list[UserImage],
        key_category_id: int = None,
        old_price: int = None,
    ) -> 'Game':
        game_in_db = await GameRepoModel.create(
            name=name,
            description=description,
            system_requirements=system_requirements,
            key_category_id=key_category_id,
            current_price=current_price,
            old_price=old_price,
            genre_id_list=genre_id_list,
        )
        game_instance = cls(game_in_db)
        await cls._store_preview_images(game_instance, images)

        return game_instance

    async def get_reviews(self) -> list['GameReview']:
        return [
            GameReview.from_db_instance(review_in_db)
            for review_in_db in await ReviewRepo.get_reviews_by_game_id(self._db_instance.id)
        ]

    async def get_preview_images(self) -> list['GamePreviewImage']:
        return [
            GamePreviewImage.from_db_instance(image_in_db)
            for image_in_db in await PreviewImageRepo.get_images_by_game_id(self._db_instance.id)
        ]

    async def update(self, **updates):
        try:
            new_images = [UserImage(**i) for i in updates.pop('new_images')]
        except KeyError:
            new_images = []
        try:
            drop_images = updates.pop('drop_images')
        except KeyError:
            drop_images = []

        await self._db_instance.update(**updates)
        if new_images is not None:
            await self._store_preview_images(new_images)
        if drop_images is not None:
            for image in filter(lambda img: img.filename in drop_images, await self.get_preview_images()):
                await image.delete()

    async def delete(self):
        game_data = await GameRepoModel.get_game_by(game_id=self._db_instance.id)
        await game_data.delete()

    @classmethod
    async def get_by(cls, game_id: int = None, alias: str = None) -> 'Game':
        game_in_db = await GameRepoModel.get_game_by(game_id=game_id, alias=alias)
        return cls(game_in_db)

    async def _store_preview_images(self, images: list[UserImage]) -> list[int]:
        game_image_ids = []
        for image in images:
            image_filename = self._generate_preview_image_filename(image)
            image_created = await GamePreviewImage.create(
                self._db_instance.id, b64decode(image.base64_encoded_source), image_filename
            )
            game_image_ids.append(image_created.id)

        return game_image_ids

    @classmethod
    def _generate_preview_image_filename(cls, img: UserImage) -> str:
        return f'{str(uuid4())}.{img.format}'
