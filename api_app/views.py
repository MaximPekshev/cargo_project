from django.shortcuts import render
import requests

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def city_list(request):
    print(request.GET)
    url = "https://api.geotree.ru/search.php?key=nhcg28MfpZ6h"
    answer = requests.get(url)
    print(answer)
    if answer:
        return answer
    else:
        return None