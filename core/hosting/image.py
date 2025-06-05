import os
from dataclasses import dataclass
from io import BytesIO
import aiofiles
import aiofiles.os


@dataclass
class StoredImage:
    path: str
    filename: str


class ImageHosting:

    def __init__(self, images_location: str | os.PathLike):
        self._images_location = images_location

    async def store_image(self, image_bytes: bytes | BytesIO, filename: str) -> StoredImage:
        final_path = os.path.join(self._images_location, filename)
        async with aiofiles.open(final_path, 'wb') as image_file:
            await image_file.write(image_bytes)

        return StoredImage(self._images_location, filename)

    async def drop_image(self, filename: str):
        await aiofiles.os.remove(os.path.join(self._images_location, filename))
