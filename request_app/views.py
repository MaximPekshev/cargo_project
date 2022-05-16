from django.shortcuts import redirect, render
import requests
from xml.etree import cElementTree as ElementTree
import ast
import math
from  cargoapp.cityCordinates import cityCordinates

# + annasoft
from decouple import config
from cargoapp.models import City
import json
from datetime import datetime
# - annasoft

url = 'https://www.atrucks.su/api/v3/carrier/get_orders'
payload = {'auth_key': config('ATRUCKS_AUTH_KEY')}
response = requests.post(url, data=payload)
data = response.text.encode("utf-8")

def getCityCordinate(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
        city.lower() +'&APPID=' + config('OPENWEATHERMAP_API_KEY')
    response = requests.post(url)
    data = response.text.encode("utf-8")
    byte_str = data
    dict_str = byte_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    dictonary = mydata
    if 'coord' in dictonary:
        lon = dictonary['coord']['lon']
        lat = dictonary['coord']['lat']
        return {'lon': lon, 'lat': lat}
    else:
        return {'lon': 0, 'lat': 0}

def getRadiusCity(city, radius):
    if city in cityCordinates:
        city_lon = cityCordinates[city]['lon']
        city_lat = cityCordinates[city]['lat']
    else:
        city_lon = getCityCordinate(city)['lon']
        city_lat = getCityCordinate(city)['lat']
    lon1 = city_lon-radius/abs(math.cos(math.radians(city_lat))*111.0)
    lon2 = city_lon+radius/abs(math.cos(math.radians(city_lat))*111.0)
    lat1 = city_lat-(radius/111.0)
    lat2 = city_lat+(radius/111.0)

    citysList = []

    for i in cityCordinates:
        city2_lon = cityCordinates[i]['lon']
        city2_lat = cityCordinates[i]['lat']
        if lon1 < city2_lon < lon2 and lat1 < city2_lat < lat2:
            citysList.append(i)

    return citysList

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                    #self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                else:
                    aDict = {element[0].tag: XmlListConfig(element)}
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})
        
if response.status_code == 200:
    root = ElementTree.XML(data)
    xmldict = XmlDictConfig(root)
else:
    print("\033[1;31m Response error:", response)
    print("\033[1;00m \n")
    xmldict = ''

#+annasoft
def index(request):
    
    return render(request, 'request_app/index.html')

def internal_index(request):
    
    return render(request, 'request_app/internal/index.html')

#-annasoft

def external_index(request):
    #+annasoft
    context = {
        'cities': City.objects.all().order_by('title'),
    }
    #-annasoft
    return render(request, 'request_app/external/index.html', context)

def order(request,order):
    url = 'https://www.atrucks.su/api/v3/carrier/get_orders'
    payload = {'auth_key': config('ATRUCKS_AUTH_KEY'),
               'order_id':order}
    response = requests.post(url, data=payload)
    data = response.text.encode("utf-8")
    root = ElementTree.XML(data)
    xmldict = XmlDictConfig(root)
    
    xmldict = ast.literal_eval(str(xmldict))
    dictonary = xmldict["{https://www.atrucks.su/xmlns/1.0}orders"]["{https://www.atrucks.su/xmlns/1.0}order"]
    
    if '{https://www.atrucks.su/xmlns/1.0}route' in dictonary:
        dictonary['route'] = dictonary['{https://www.atrucks.su/xmlns/1.0}route']['{https://www.atrucks.su/xmlns/1.0}waypoint']
        del dictonary['{https://www.atrucks.su/xmlns/1.0}route']

    # print(dictonary)
    return render(request, 'request_app/external/order.html',{'data':dictonary})


def getAll(request):
    global xmldict     

    # get 
    xmldict = ast.literal_eval(str(xmldict))
    dictonary = xmldict["{https://www.atrucks.su/xmlns/1.0}orders"]["{https://www.atrucks.su/xmlns/1.0}order"]
    for i in dictonary:
        if '{https://www.atrucks.su/xmlns/1.0}route' in i:
            i['route'] = i['{https://www.atrucks.su/xmlns/1.0}route']['{https://www.atrucks.su/xmlns/1.0}waypoint']
            del i['{https://www.atrucks.su/xmlns/1.0}route']

    filtredDict = []
    for i in range(0,len(dictonary),2):
        filtredDict.append(dictonary[i])
        
    return render(request, 'request_app/external/search.html',{'date':filtredDict})
    
    
def search(request,param):
    global xmldict     
    
    # + annasoft
    if request.method == 'GET':
        input_city = request.GET.get('city')

        if request.GET.get('load'):
            input_load = request.GET.get('load')
        else:
            input_load = None

        if request.GET.get('radius'):
            input_radius = int(request.GET.get('radius'))
        else:
            input_radius = None    

        if input_radius:
            cityList = getRadiusCity(input_city.lower(), input_radius)
            torgtrans_data = []
            for city in cityList:
                torgtrans_acive_data = get_torgtrans_active_data(city, input_load)
                torgtrans_data += torgtrans_acive_data
                torgtrans_acive_ffa_data = get_torgtrans_active_ffa_data(city, input_load)
                torgtrans_data += torgtrans_acive_ffa_data
        else:
            torgtrans_acive_data = get_torgtrans_active_data(input_city, input_load)
            torgtrans_acive_ffa_data = get_torgtrans_active_ffa_data(input_city, input_load)
            torgtrans_data = torgtrans_acive_data + torgtrans_acive_ffa_data
    # - annasoft

    url = param
    if ';' in url or 'city=' in url or 'load=' in url:
        url = param.split(';')

    load = ''
    city = ''
    radius = ''
    for i in url:
        if 'city' in i:
            city = i.split('city=')[1].lower()
        if 'radius' in i:
            radius = int(i.split('radius=')[1])
        if 'load' in i:
            load = i.split('load=')[1]
            
    if city and radius:
        # print(city, type(city))
        # print(radius, type(radius))
        cityList = getRadiusCity(city, radius)
    # get
    filtredDict = []
    if xmldict:
        xmldict = ast.literal_eval(str(xmldict))
        dictonary = xmldict["{https://www.atrucks.su/xmlns/1.0}orders"]["{https://www.atrucks.su/xmlns/1.0}order"]
        for i in dictonary:
            if '{https://www.atrucks.su/xmlns/1.0}route' in i:
                i['route'] = i['{https://www.atrucks.su/xmlns/1.0}route']['{https://www.atrucks.su/xmlns/1.0}waypoint']
                del i['{https://www.atrucks.su/xmlns/1.0}route']

        for i in range(0, len(dictonary), 2):
            filtredDict.append(dictonary[i])

        if city and not load and not radius:
            filterList = []
            for i in filtredDict:
                for j in i['route']:
                    cityName = city.lower()[0].upper() + city.lower()[1:]
                    if cityName in j['address']['free_form']:
                        if i not in filterList:
                            filterList.append(i)   

            return render(request, 'request_app/external/search.html',{'date':filterList, 'status':response.status_code, 'torgtrans_data' : torgtrans_data})
        
        elif city and load and not radius:
            filterList = []
            for i in filtredDict:
                if 'route' in i.keys():
                    for j in i['route']:
                        cityName = city.lower()[0] + city.lower()[1:]
                        if cityName in j['address']['free_form'] and j['waypoint_type'] == load:
                            if i not in filterList:
                                filterList.append(i)  

            return render(request, 'request_app/external/search.html',{'date':filterList, 'status':response.status_code, 'torgtrans_data' : torgtrans_data})
        
        elif city and not load and radius:
            filterList = []
            
            for i in filtredDict:
                if 'route' in i.keys():
                    for j in i['route']:                    
                        for c in cityList:
                            cityName = c.lower()[0].upper() + c.lower()[1:]
                            if cityName in j['address']['free_form']:
                                if i not in filterList:
                                    filterList.append(i)

            return render(request, 'request_app/external/search.html',{'date':filterList, 'status':response.status_code, 'torgtrans_data' : torgtrans_data})

        elif city and load and radius:
            filterList = []
            for i in filtredDict:
                if 'route' in i.keys():
                    for j in i['route']:                    
                        for c in cityList:
                            cityName = c.lower()[0].upper() + c.lower()[1:]
                            if cityName in j['address']['free_form']:
                                if i not in filterList:
                                    filterList.append(i)

            return render(request, 'request_app/external/search.html',{'date':filterList, 'status':response.status_code, 'torgtrans_data' : torgtrans_data})                            

    
    return render(request, 'request_app/external/search.html',{'date':filtredDict, 'status':response.status_code, 'torgtrans_data' : torgtrans_data})


def searchRedir(request):
    return redirect('/search/')


def get_torgtrans_active_data(input_city, input_load):

    url = config('TORGTRANS_MAIN_URL')
    headers = {config('TORGTRANS_API_KEY_NAME'):config('TORGTRANS_AUTH_KEY')}

    data = """
            query{
                order_list(category: "active"){
                data{
                    id
                    status
                    comment
                    client_company{
                        name
                    }
                    client_user{
                        name
                        surname
                    }
                    auction{
                        end_date
                        current_date
                        currency
                        created_at
                        start_gross_price
                    }
                    loading_depots{
                        id
                        date_start
                        date_end
                        contact_name
                        contact_company
                        contact_phone
                        location{
                            formatted
                            region
                            city
                            street
                            number
                        }
                    }
                    unloading_depots{
                        id
                        date_start
                        date_end
                        contact_name
                        contact_company
                        contact_phone
                        location{
                            formatted
                            region
                            city
                            street
                            number
                        }
                    }
                }
            }
        }"""
    
    answer = requests.post(url, headers=headers, json={'query': data})
    response = answer.json()
    current_order_list = []
    try:
        order_list = response.get('data').get('order_list').get('data')
    except:
        return current_order_list

    if order_list:
        if input_load:
            for order in order_list:
                order = correct_time(order)
                if input_load == 'unloading':
                    for depo in order.get('unloading_depots'):
                        if input_city in depo.get('location').get('formatted'):
                            if order.get('status') == 500 and not order in current_order_list:
                                current_order_list.append(order)
                elif input_load == 'loading':
                    for depo in order.get('loading_depots'):
                        if input_city in depo.get('location').get('formatted'):
                            if order.get('status') == 500 and not order in current_order_list:
                                current_order_list.append(order)

        else:
            for order in order_list:
                order = correct_time(order)
                for depo in order.get('loading_depots'):
                    if input_city in depo.get('location').get('formatted'):
                        if order.get('status') == 500 and not order in current_order_list:
                            current_order_list.append(order)
                            
                for depo in order.get('unloading_depots'):
                    if input_city in depo.get('location').get('formatted'):
                        if order.get('status') == 500 and not order in current_order_list:
                            current_order_list.append(order)

    return current_order_list

def get_torgtrans_active_ffa_data(input_city, input_load):

    url = config('TORGTRANS_MAIN_URL')
    headers = {config('TORGTRANS_API_KEY_NAME'):config('TORGTRANS_AUTH_KEY')}

    data = """
            query{
                order_list(category: "active_ffa"){
                data{
                    id
                    status
                    comment
                    client_company{
                        name
                    }
                    client_user{
                        name
                        surname
                    }
                    auction{
                        end_date
                        current_date
                        currency
                        created_at
                        start_gross_price
                    }
                    loading_depots{
                        id
                        date_start
                        date_end
                        contact_name
                        contact_company
                        contact_phone
                        location{
                            formatted
                            region
                            city
                            street
                            number
                        }
                    }
                    unloading_depots{
                        id
                        date_start
                        date_end
                        contact_name
                        contact_company
                        contact_phone
                        location{
                            formatted
                            region
                            city
                            street
                            number
                        }
                    }
                }
            }
        }"""
    
    answer = requests.post(url, headers=headers, json={'query': data})
    response = answer.json()
    current_order_list = []
    try:
        order_list = response.get('data').get('order_list').get('data')
    except:
        return current_order_list

    if order_list:
        if input_load:
            for order in order_list:
                order = correct_time(order)
                if input_load == 'unloading':
                    for depo in order.get('unloading_depots'):
                        if input_city in depo.get('location').get('formatted'):
                            if order.get('status') == 500 and not order in current_order_list:
                                current_order_list.append(order)
                elif input_load == 'loading':
                    for depo in order.get('loading_depots'):
                        if input_city in depo.get('location').get('formatted'):
                            if order.get('status') == 500 and not order in current_order_list:
                                current_order_list.append(order)

        else:
            for order in order_list:
                order = correct_time(order)
                for depo in order.get('loading_depots'):
                    if input_city in depo.get('location').get('formatted'):
                        if order.get('status') == 500 and not order in current_order_list:
                            current_order_list.append(order)
                            
                for depo in order.get('unloading_depots'):
                    if input_city in depo.get('location').get('formatted'):
                        if order.get('status') == 500 and not order in current_order_list:
                            current_order_list.append(order)

    return current_order_list

def correct_time(order):
    for depo in order.get('unloading_depots'):

        if depo["date_start"]:
            depo["date_start"] = datetime.utcfromtimestamp(int(depo.get("date_start"))).strftime("%Y-%m-%d %H:%M:%S")
        if depo["date_end"]:
            depo["date_end"] = datetime.utcfromtimestamp(int(depo.get("date_end"))).strftime("%Y-%m-%d %H:%M:%S")                             

    for depo in order.get('loading_depots'):

        if depo["date_start"]:
            depo["date_start"] = datetime.utcfromtimestamp(int(depo.get("date_start"))).strftime("%Y-%m-%d %H:%M:%S")
        if depo["date_end"]:    
            depo["date_end"] = datetime.utcfromtimestamp(int(depo.get("date_end"))).strftime("%Y-%m-%d %H:%M:%S")     

    return order    
