import requests
from ..models import APIEndpoints


# yapılacaklar servis api endpointleri dbye kaydedilsin dbdn gelsin auth header required false true gelsin



class CryptoMarketPlace():
    def __init__(self):
        self.timestamp = None
        self.db_model = None
        self.domain = None
        self.api_model = APIEndpoints

    def generate_headers(self, url=None, params=None):
        return None
    

    def get_api_endpoints(self, website):
        return APIEndpoints.objects.filter(api_site_name=website)


    def fetcher(self, auth_header_required=False, url=None, method=None, params=None):
        if params:
            if auth_header_required:
                headers = self.generate_headers(params)
                response = requests.request(method, self.domain + url + '?' + params, headers=headers)
            else:
                response = requests.request(method, self.domain + url)
        else:
            if auth_header_required:
                headers = self.generate_headers(url)
                response = requests.request(method, self.domain + url, headers=headers)
            else:
                response = requests.request(method, self.domain + url)
        
        return response.json()
    


