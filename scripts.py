import xlrd
from cargoapp.models import City, Vehicle, Driver
from cargoapp.cityCordinates import cityCordinates
from decouple import config
import requests
import ast
import time
from datetime import datetime

def import_cities():

    book = xlrd.open_workbook("city.xls")
    sh = book.sheet_by_index(0)

    for rx in range(sh.nrows):
        
        sh.cell(rx, 1)
        
        city = City(

            code = str(sh.cell_value(rx, 2)).split('.')[0],
            title =  sh.cell_value(rx, 0),
            reduction = sh.cell_value(rx, 1),

        )

        city.save()

def import_coordinates():

    for city in cityCordinates:
        
        strCity = city
        strLon = cityCordinates.get(city).get('lon')
        strLat = cityCordinates.get(city).get('lat')

        try:
            bd_city = City.objects.filter(title=strCity.capitalize()).first()
        except City.DoesNotExist:
            bd_city = City(
                code = strCity.capitalize(),
                title = strCity.capitalize(),
                reduction = 'г',
            )
            bd_city.save()

        if bd_city:
            bd_city.lon = strLon
            bd_city.lat = strLat
            bd_city.save()

def import_coordinates_from_api():

    for city in City.objects.all():
        if not city.lon or not city.lat:
            time.sleep(3)
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            city.title.lower() +'&APPID='+ config('OPENWEATHERMAP_API_KEY')
            response = requests.post(url)
            data = response.text.encode("utf-8")
            dict_str = data.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            dictionary = mydata
            if 'coord' in dictionary:
                lon = dictionary['coord']['lon']
                lat = dictionary['coord']['lat']
                city.lon = lon
                city.lat = lat
                city.save()




def import_nav_id():

    book = xlrd.open_workbook("vin_id.xls")
    sh = book.sheet_by_index(0)

    for rx in range(sh.nrows):

        try: 
            vehicle = Vehicle.objects.get(vin=sh.cell(rx, 0).value)
            vehicle.nav_id = str(int(sh.cell(rx, 1).value))
            vehicle.save()
            print('nav_id: ' + str(int(sh.cell(rx, 1).value)) + ' записан в БД')
        except:
            print('Автомобиль с VIN: ' + sh.cell(rx, 0).value + ' в базе данных не найден')
                

def import_employment_date():

    book = xlrd.open_workbook("tempfiles/drivers.xls")
    sh = book.sheet_by_index(0)

    for rx in range(sh.nrows):

        try:
            driver = Driver.objects.get(uid=str(sh.cell(rx, 0).value))
            driver.employment_date = datetime.strptime(sh.cell(rx, 1).value, '%Y-%m-%d')
            driver.save()
            print('driver:' + driver.title + '. employment_date: ' + sh.cell(rx, 1).value + ' записан в БД')
        except:
            print('Водитель с UID: ' + sh.cell(rx, 0).value + ' в базе данных не найден')
