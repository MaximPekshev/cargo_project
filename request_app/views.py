from django.shortcuts import redirect, render
import requests
from xml.etree import cElementTree as ElementTree
import ast

# + annasoft
from decouple import config
from cargoapp.models import City
# - annasoft

url = 'https://www.atrucks.su/api/v3/carrier/get_orders'
payload = {'auth_key': config('ATRUCKS_AUTH_KEY')}
response = requests.post(url, data=payload)
data = response.text.encode("utf-8")


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
        


root = ElementTree.XML(data)
xmldict = XmlDictConfig(root)

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
    
    url = param
    if ';' in url or 'city=' in url or 'load=' in url:
        url = param.split(';')
    
    load = ''
    city = ''
    for i in url:
        if 'city' in i:
            city = i.split('city=')[1]   
            # print(city) 
        if 'radius' in i:
            radius = i.split('radius=')[1]
            
        if 'load' in i:
            load = i.split('load=')[1]
            # print(load)
            



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
    
    if city and not load:
        filterList = []
        for i in filtredDict:            
            for j in i['route']:
                if city.lower() in j['address']['free_form'].lower():
                    filterList.append(i)
                    
        return render(request, 'request_app/external/search.html',{'date':filterList})
    
    elif city and load:
        filterList = []
        for i in filtredDict:            
            if 'route' in i.keys():
                for j in i['route']:
                    if city.lower() in j['address']['free_form'].lower() and j['waypoint_type'] == load:
                        filterList.append(i)
                    
        return render(request, 'request_app/external/search.html',{'date':filterList})
        

    
    return render(request, 'request_app/external/search.html',{'date':filtredDict})


def searchRedir(request):
    return redirect('/search/')
