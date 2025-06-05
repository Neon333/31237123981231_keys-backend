import config
from .image import ImageHosting


def get_image_hosting() -> ImageHosting:
    return ImageHosting(config.IMAGE_HOST_PATH)
