import hashlib
from urllib.parse import urlencode


class FreeKassaAsyncClient:
    BASE_URL = "https://pay.freekassa.ru/"

    def __init__(self, merchant_id: str, secret_word: str, secret_word_2: str, currency: str = "RUB"):
        self.merchant_id = merchant_id
        self.secret_word = secret_word
        self.secret_word_2 = secret_word_2  # Используется для валидации платежей
        self.currency = currency

    def generate_payment_form(self, amount: float | int, order_id: str) -> str:
        sign = hashlib.md5(f"{self.merchant_id}:{amount}:{self.secret_word}:{self.currency}:{order_id}".encode()).hexdigest()

        params = {
            "m": self.merchant_id,
            "oa": amount,
            "o": order_id,
            "currency": self.currency,
            "s": sign,
            "us_order_id": order_id,
        }

        form_html = f"""
        <form action="{self.BASE_URL}" method="GET">
            {"".join(f'<input type="hidden" name="{k}" value="{v}"/>' for k, v in params.items())}
            <button type="submit">Оплатить</button>
        </form>
        """
        return form_html

    def validate_signature(self, merchant_id: str, amount: float, order_id: str, received_sign: str) -> bool:
        expected_sign = hashlib.md5(f"{merchant_id}:{amount}:{self.secret_word_2}:{order_id}".encode()).hexdigest()
        return expected_sign == received_sign
