from . import CryptoMarketPlace
from ..models import OkxAPI
from ..utilities import okx_signature, decode
import datetime as dt
from asgiref.sync import sync_to_async



class OKX(CryptoMarketPlace):
    def __init__(self, user):
        self.timestamp = dt.datetime.utcnow().isoformat()[:-3]+'Z'
        self.user = user
        self.db_model = OkxAPI
        self.domain = 'https://www.okx.com'
    

    async def generate_headers(self, url=None, params=None):
        api_info = await sync_to_async(OkxAPI.objects.get)(user=self.user)

        message = self.timestamp + 'GET' + url

        headers = {
            'OK-ACCESS-TIMESTAMP': self.timestamp,
            'OK-ACCESS-KEY': decode(api_info.api_key),
            'OK-ACCESS-PASSPHRASE': decode(api_info.access_passphrase),
            'OK-ACCESS-SIGN': okx_signature(decode(api_info.secret_key), message)
        }

        return headers
    

    async def get_api_data(self):
        context = {}

        api_endpoints = await self.get_api_endpoints('okx')

        for endpoint in api_endpoints:
            context[endpoint.endpoint_name] = await self.fetcher(endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method)

        return context
