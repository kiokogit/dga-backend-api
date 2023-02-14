import json
import urllib
import requests

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class GetCountriesData(GenericViewSet):

    @action(detail=False, methods=['GET'])
    def get_countries_data(self, request):
        # where = urllib.parse.quote_plus("""{"name":{"$regex": "%s"}}"""%request.query_params.get("name"))        # type: ignore  
        url = 'https://parseapi.back4app.com/classes/Continentscountriescities_Country?limit=300&order=name&excludeKeys=capital,continent,native,shape'

        headers = {
            'X-Parse-Application-Id': '5vg4Ews4qq2Q3Akc9CxfgeMSFyjEsCl5fcKJ7YSX', # This is your app's application id
            'X-Parse-REST-API-Key': 'jbHtR8M73llNcp9bzjrVWSW7vf4MYYtOmjqxmN6M' # This is your app's REST API key
        }
        data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_cities_towns(self, request):

        url = f"https://api.countrystatecity.in/v1/countries/{request.query_params.get('code')}/cities"

        headers = {
        'X-CSCAPI-KEY': 'WE5ub1lWbTV5ZTRaVU54QlJIb2V3TXBkNFRxUWNlQW1XU3p5MXNoTA=='
        }

        response = json.loads(requests.request("GET", url, headers=headers).content.decode('utf-8'))

        return Response(response, status=status.HTTP_200_OK)
