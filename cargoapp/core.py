import requests
import json
from decouple import config
import datetime
from decimal import Decimal
import xlrd

def upload_route(route):
    if route:

        url = 'http://1c.annasoft.ru:8081/test/hs/cargo/api/v1/routes'
        header = {'Authorization' : config('1C_API_SECRET_KEY')}

        data = {
            "fields": {
                "uid" : route.uid,
                "from_date" : route.from_date.strftime('%Y%m%d000000'),
                "to_date" : route.to_date.strftime('%Y%m%d000000'),
                "a_point" : route.a_point,
                "b_point" : route.b_point,
                "length" : str(Decimal(route.route_length)),
                "cost" : str(Decimal(route.route_cost)),
                "expenses_1" : str(Decimal(route.expenses_1)),
                "expenses_2" :str(Decimal(route.expenses_2)),
                "expenses_3" : str(Decimal(route.expenses_3)),
                "weight" : str(Decimal(route.weight)),
                "request_number" : route.request_number,
                "description" : route.cargo_description,

            },
            "vehicle": {
                "uid" : route.get_vehicle(),
            },
            "driver" : {
                "uid" : route.get_driver(),
            },
            "logist" : {
                "uid" : route.get_logist(),
            },
            "client" : {
                "uid" : route.get_client(),
            }
        }

        answer = requests.post(url, headers=header, data=json.dumps(data))
        print(answer.status_code)

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def first_day_of_the_month(any_day):
    if any_day.day > 25:
        any_day += datetime.timedelta(7)
    return any_day.replace(day=1)
