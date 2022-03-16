import requests
import json
from decouple import config
from decimal import Decimal

def upload_accrual(accrual_deduction):

    if accrual_deduction:

        if accrual_deduction.type == '1':
            url = config('1C_ADDRESS') + 'api/v1/accrual'
        elif accrual_deduction.type == '0':
            url = config('1C_ADDRESS') + 'api/v1/deduction'
        
        header = {'Authorization' : config('1C_API_SECRET_KEY')}

        data = {
            "fields": {
                "uid" : accrual_deduction.uid,
                "date" : accrual_deduction.date.strftime('%Y%m%d000000'),
                "sum": str(Decimal(accrual_deduction.sum)),
            },
            "vehicle": {
                "uid" : accrual_deduction.get_vehicle(),
            },
            "driver" : {
                "uid" : accrual_deduction.get_driver(),
            },
            "logist" : {
                "uid" : accrual_deduction.get_logist(),
            }
        }

        answer = requests.post(url, headers=header, data=json.dumps(data))
        if answer.status_code == 200:
            # print(answer.status_code)
            accrual_deduction.upload_status = True
            accrual_deduction.save()