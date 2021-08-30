import requests
import json
from decouple import config
import datetime
from decimal import Decimal

def upload_route(route):
    
    if route:

        url = 'http://1c.annasoft.ru:8081/test/hs/cargo/api/v1/routes'
        header = {'Authorization' : config('1C_API_SECRET_KEY')}

        data = {
            "fields": {
                "uid" : route.uid,
                "from_date" : route.from_date.strftime('%Y-%m-%d'),
                "to_date" : route.to_date.strftime('%Y-%m-%d'),
                "a_point" : route.a_point,
                "b_point" : route.b_point,
                "length" : str(Decimal(route.route_length)),
                "cost" : str(Decimal(route.route_cost)),
                "expenses_1" : str(Decimal(route.expenses_1)),
                "expenses_2" :str(Decimal(route.expenses_2)),
                "expenses_3" : str(Decimal(route.expenses_3)),

            },
            "vehicle": {
                "uid" : route.get_vehicle(),
            },
            "driver" : {
                "uid" : route.get_driver(),
            },
            "logist" : {
                "uid" : route.get_logist(),
            }
        }
        print(data)
        # json.dumps(data)

        answer = requests.post(url, headers=header, data=json.dumps(data),)
        print(answer.status_code)