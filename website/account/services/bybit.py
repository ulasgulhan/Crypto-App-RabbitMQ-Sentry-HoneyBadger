import asyncio
import aiohttp
from . import CryptoMarketPlace
from ..utilities import bybit_signature, decode
from asgiref.sync import sync_to_async
from pybit.unified_trading import HTTP


class Bybit(CryptoMarketPlace):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.domain = 'https://api.bybit.com'
        self.session = HTTP(testnet=True)
    

    
    async def generate_headers(self, url=None, params=''):
        api_info = await sync_to_async(self.db_model.objects.get)(user=self.user, crypto_market=2)
        api_key = decode(api_info.api_key)
        time = self.session.get_server_time()
        message = str(time['time']) + api_key + str(5000) + params

        headers = {
            'X-BAPI-TIMESTAMP': str(time['time']),
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-RECV-WINDOW': str(5000),
            'X-BAPI-SIGN': bybit_signature(decode(api_info.secret_key), message)
        }

        return headers
    
    async def get_api_data(self):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints(2)

            tasks = []
            for endpoint in api_endpoints:
                tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=endpoint.endpoint_params))

            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context