import requests
import json
from decouple import config
import datetime
from decimal import Decimal

PAYMENT_TYPE = {
	'0': 'Наличная',
	'1': 'Безналичная',
	'2': 'По заявке',
}

def upload_route(route):
    if route:
        
        url = config('1C_ADDRESS') + 'api/v1/routes'
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
                "straight" : str(Decimal(route.straight)),
                "fuel_cost" : str(Decimal(route.fuel_cost)),
                "pay_check" : str(Decimal(route.pay_check)),
                "pure_income" : str(Decimal(route.pure_income)),
                "cost_of_km" : str(Decimal(route.cost_of_km)),
                "cost_of_platon" : str(Decimal(route.cost_of_platon)),
                "day_count" : str(Decimal(route.day_count)),
                "payment_type": PAYMENT_TYPE.get(route.payment_type),
                "banner_a": route.banner_a,
                "banner_b": route.banner_b,
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
            },
            "contract" : {
                "uid" : route.get_contract(),
            },
            "organization" : {
                "uid" : route.get_organization(),
            },

        }

        answer = requests.post(url, headers=header, data=json.dumps(data))
        # print(answer.status_code)

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def first_day_of_the_month(any_day):
    if any_day.day > 25:
        any_day += datetime.timedelta(7)
    return any_day.replace(day=1)
