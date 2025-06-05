import aiohttp
import hashlib
import hmac
import json
import time


class NicePayAsyncClient:

    def __init__(self, merchant_id: str, merchant_key: str, base_url: str = 'https://api.nicepay.io/v1/'):
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.base_url = base_url

    def _generate_signature(self, params: dict) -> str:
        message = json.dumps(params, separators=(',', ':'))
        signature = hmac.new(self.merchant_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return signature

    async def create_payment(self, amount: float, currency: str, order_id: str, return_url: str, **kwargs) -> dict:
        url = f'{self.base_url}payments'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Merchant-ID': self.merchant_id,
            'Request-Time': str(int(time.time())),
        }
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'return_url': return_url,
            **kwargs
        }

        headers['Signature'] = self._generate_signature(data)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                return await response.json()

    async def get_payment_status(self, payment_id: str) -> dict:
        url = f'{self.base_url}payments/{payment_id}'
        headers = {
            'Merchant-ID': self.merchant_id,
            'Request-Time': str(int(time.time())),
            'Signature': self._generate_signature({'payment_id': payment_id})
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
