import requests
import json
from decouple import config
# import datetime
# from decimal import Decimal

def upload_line_release(line_release):
    if line_release:
        
        url = config('1C_ADDRESS') + 'api/v1/line-release'
        header = {'Authorization' : config('1C_API_SECRET_KEY')}
        data = {
            "fields": {
                "uid" : line_release.uid,
                "release_date" : line_release.release_date.strftime('%Y%m%d%H%M%S'),
                "begin_date" : line_release.begin_date.strftime('%Y%m%d%H%M%S'),
                "end_date" : line_release.end_date.strftime('%Y%m%d%H%M%S'),
                "renewal" : line_release.renewal,
                "for_repair" : line_release.for_repair,
            },
            "vehicle": {
                "uid" : line_release.get_vehicle(),
            },
            "driver" : {
                "uid" : line_release.get_driver(),
            },
            "columnar" : {
                "uid" : line_release.get_columnar(),
            },
            "trailer" : {
                "uid" : line_release.get_trailer(),
                "vin" : line_release.get_trailer_vin(),
            },
            

        }
        answer = requests.post(url, headers=header, data=json.dumps(data))