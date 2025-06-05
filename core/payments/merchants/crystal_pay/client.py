from urllib.parse import urlparse, parse_qs

import aiohttp
import hashlib
import hmac


class CrystalPayAsyncClient:
    def __init__(self, auth_login: str, auth_secret: str, salt: str):
        self.auth_login = auth_login
        self.auth_secret = auth_secret
        self.base_url = 'https://api.crystalpay.io/v3/'
        self.salt = salt  # Секретный ключ salt

    async def create_invoice(self, amount: float, invoice_type: str, lifetime: int, **kwargs) -> dict:
        url = f'{self.base_url}invoice/create/'
        data = {
            'auth_login': self.auth_login,
            'auth_secret': self.auth_secret,
            'amount': amount,
            'type': invoice_type,
            'lifetime': lifetime,
            **kwargs
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()

    async def generate_payment_form(self, amount: float, invoice_type: str, lifetime: int, **kwargs) -> str:
        url = 'https://pay.crystalpay.io'
        new_invoice_json = await self.create_invoice(amount, invoice_type, lifetime, **kwargs)
        parsed_url = urlparse(new_invoice_json['url'])
        params = parse_qs(parsed_url.query)
        invoice_id = params.get('i', [None])[0]

        form_html = f"""
        <form action="{url}" method="GET">
            <input type="hidden" name="i" value="{invoice_id}">
            <button type="submit">Оплатить</button>
        </form>
        """
        return form_html

    async def get_invoice_info(self, invoice_id: str) -> dict:
        url = f'{self.base_url}invoice/info/'
        data = {
            'auth_login': self.auth_login,
            'auth_secret': self.auth_secret,
            'id': invoice_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()

    def verify_signature(self, _id: int, signature: str) -> bool:
        hash_string = f"{_id}:{self.salt}"
        computed_hash = hashlib.sha1(hash_string.encode()).hexdigest()

        return hmac.compare_digest(computed_hash, signature)
