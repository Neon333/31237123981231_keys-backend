import config
from core.payments.merchants.crystal_pay.client import CrystalPayAsyncClient
from core.payments.merchants.free_kassa.sync_clinet import FreeKassaAsyncClient


def get_freekassa_client() -> FreeKassaAsyncClient:
    return FreeKassaAsyncClient(
        merchant_id=config.FREEKASSA_MERCHANT_ID,
        secret_word=config.FREEKASSA_SECRET_1,
        secret_word_2=config.FREEKASSA_SECRET_2
    )


def get_crystalpay_client() -> CrystalPayAsyncClient:
    return CrystalPayAsyncClient(
        auth_login=config.CRYSTALPAY_LOGIN,
        auth_secret=config.CRYSTALPAY_SECRET,
        salt=config.CRYSTALPAY_SALT
    )
