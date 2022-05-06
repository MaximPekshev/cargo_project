import xlrd
from cargoapp.models import City, Vehicle, Driver, Trailer
from insurance_app.models import VehicleInsurance, ContragentInsurance, OwnerInsurance, TrailerInsurance
from cargoapp.cityCordinates import cityCordinates
from decouple import config
import requests
import ast
import time
from datetime import datetime

def import_cities():
    # from scripts import import_cities
    book = xlrd.open_workbook("tempfiles/addresses.xlsx")
    sh = book.sheet_by_index(0)

    for rx in range(sh.nrows):

    
        city = City.objects.filter(title=sh.cell_value(rx, 3)).first()

        if city:

            city.region_code = sh.cell_value(rx, 0)
            city.save()

        else:
            
            if sh.cell_value(rx, 3):
                city = City(
                    title =  sh.cell_value(rx, 3),
                    reduction = sh.cell_value(rx, 1),
                    region_code = str(sh.cell_value(rx, 0)).split(".")[0],
                )
                if type(sh.cell_value(rx, 2)) is float:
                    code = str(sh.cell_value(rx, 2)).split(".")[0]
                elif type(sh.cell_value(rx, 2))is str:
                    code = sh.cell_value(rx, 2).replace(" ", "")
                else:
                    code = None    

                if code:
                    code_city = City.objects.filter(code=code).first()
                    if not code_city:
                        city.code = code
                        city.save()  
                        print(sh.cell_value(rx, 3) + ' успешно записан в БД')

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
            time.sleep(1)
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

def import_nav_id_by_car_number():

    book = xlrd.open_workbook("tempfiles/nav_id.xls")
    sh = book.sheet_by_index(0)

    for rx in range(sh.nrows):

        try: 
            vehicle = Vehicle.objects.get(car_number=sh.cell(rx, 0).value)
            vehicle.nav_id = str(int(sh.cell(rx, 1).value))
            vehicle.save()
            print('nav_id: ' + str(int(sh.cell(rx, 1).value)) + ' записан в БД')
        except:
            print('Автомобиль с номером: ' + sh.cell(rx, 0).value + ' в базе данных не найден')
                

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


def import_insurance_contract():

    book = xlrd.open_workbook("tempfiles/insurance.xlsx")
    sh = book.sheet_by_index(0)
    for rx in range(sh.nrows):

        # car_number =  sh.cell_value(rx, 0) #str
        car_title = sh.cell_value(rx, 1) #str
        car_year = sh.cell_value(rx, 2) #str 2016(2)
        car_vin = sh.cell_value(rx, 3) #str 
        if sh.cell_value(rx, 4) != '-':
            osago_date_to = datetime(*xlrd.xldate_as_tuple(sh.cell_value(rx, 4), 0)).date() #datetime 
        else:
            osago_date_to = None             
        osago_contragent = sh.cell_value(rx, 5) #str 
        if sh.cell_value(rx, 6) != '-':
            if type(sh.cell_value(rx, 6)) is float:
                casco_date_to = datetime(*xlrd.xldate_as_tuple(sh.cell_value(rx, 6), 0)).date() #datetime 
            elif type(sh.cell_value(rx, 6)) is str:
                casco_date_to = datetime.strptime(sh.cell_value(rx, 6), '%d.%m.%Y').date()
            else:
                casco_date_to = None     
        if sh.cell_value(rx, 7) != '-':
            if type(sh.cell_value(rx, 7)) is float:
                casco_date_from = datetime(*xlrd.xldate_as_tuple(sh.cell_value(rx, 7), 0)).date() #datetime 
            elif type(sh.cell_value(rx, 7)) is str:
                casco_date_from = datetime.strptime(sh.cell_value(rx, 7), '%d.%m.%Y').date()
            else:    
                casco_date_from = None     
        casco_contragent = sh.cell_value(rx, 8) #str

        owner_contragent = sh.cell_value(rx, 9) #str
        
        vehicle = Vehicle.objects.filter(vin=car_vin).first()
        if vehicle:
            
            vehicle.title = car_title
            if car_year:
                release_date = car_year.split('(')[0]
                consignment = car_year.split('(')[1][0]
                release_date = release_date + '.01.01'
                vehicle.release_date = datetime.strptime(release_date, '%Y.%m.%d').date()
                vehicle.consignment = consignment
                vehicle.save()

            if osago_date_to:
                try:
                    contragnt_insurance = ContragentInsurance.objects.get(title = osago_contragent.upper())
                except ContragentInsurance.DoesNotExist:
                    contragnt_insurance = ContragentInsurance(title=osago_contragent.upper())
                    contragnt_insurance.save()

                try:
                    owner_insurance = OwnerInsurance.objects.get(title = owner_contragent.upper())
                except OwnerInsurance.DoesNotExist:
                    owner_insurance = OwnerInsurance(title=owner_contragent.upper())
                    owner_insurance.save()    
    
                new_osago_vehicle_insurance = VehicleInsurance(
                    vehicle=vehicle,
                    type='0',
                    to_date=osago_date_to,
                    contragent=contragnt_insurance,
                    owner=owner_insurance,
                )
                new_osago_vehicle_insurance.save()

            if casco_date_from:

                try:
                    contragnt_insurance = ContragentInsurance.objects.get(title = casco_contragent.upper())
                except ContragentInsurance.DoesNotExist:
                    contragnt_insurance = ContragentInsurance(title=casco_contragent.upper())
                    contragnt_insurance.save()

                try:
                    owner_insurance = OwnerInsurance.objects.get(title = owner_contragent.upper())
                except OwnerInsurance.DoesNotExist:
                    owner_insurance = OwnerInsurance(title=owner_contragent.upper())
                    owner_insurance.save()    

                new_casco_vehicle_insurance = VehicleInsurance(
                    vehicle=vehicle,
                    type='1',
                    from_date = casco_date_from,
                    to_date=casco_date_to,
                    contragent=contragnt_insurance,
                    owner=owner_insurance,
                )
                new_casco_vehicle_insurance.save()    
                    

        else:
            print('Автомобиля с vin: ' + car_vin + ' нет в БД')


def import_trailer_insurance_contract():

    book = xlrd.open_workbook("tempfiles/insurance.xlsx")
    sh = book.sheet_by_index(1)
    for rx in range(sh.nrows):

        trailer_number =  sh.cell_value(rx, 0).replace(' ', '')#str
        trailer_title = sh.cell_value(rx, 1) #str
        trailer_year = sh.cell_value(rx, 2) #str 2016(2)
        trailer_vin = sh.cell_value(rx, 3) #str 
        if sh.cell_value(rx, 4) != '-':
            if type(sh.cell_value(rx, 4)) is float:
                casco_date_to = datetime(*xlrd.xldate_as_tuple(sh.cell_value(rx, 4), 0)).date() #datetime
            elif type(sh.cell_value(rx, 4)) is str:
                casco_date_to = datetime.strptime(sh.cell_value(rx, 4), '%d.%m.%Y').date()         
        else:
            casco_date_to = None             
        if sh.cell_value(rx, 5) != '-':
            if type(sh.cell_value(rx, 5)) is float:
                casco_date_from = datetime(*xlrd.xldate_as_tuple(sh.cell_value(rx, 5), 0)).date() #datetime
            elif type(sh.cell_value(rx, 5)) is str:
                casco_date_from = datetime.strptime(sh.cell_value(rx, 5), '%d.%m.%Y').date() 
        else:
            casco_date_from = None
        if sh.cell_value(rx, 6) != '-': 
            casco_contragent = str(sh.cell_value(rx, 6)) #str
        else:
            casco_contragent = None
        if sh.cell_value(rx, 7) != '-': 
            owner_contragent = str(sh.cell_value(rx, 7)) #str
        else:
            owner_contragent = None
        
        trailer = Trailer.objects.filter(vin=trailer_vin).first()
        if not trailer:
            if type(sh.cell_value(rx, 2)) is float:
                trailer_year = str(trailer_year)
            if trailer_year:
                release_date = trailer_year.split('(')[0].split('.')[0]
                try:
                    consignment = trailer_year.split('(')[1][0]
                except:
                    consignment = ''

                release_date = release_date + '.01.01'

            trailer = Trailer(
                vin= trailer_vin,
                number=trailer_number,
                title=trailer_title,
                release_date = datetime.strptime(release_date, '%Y.%m.%d').date(),
                consignment = consignment,
            )
            trailer.save()

        if casco_date_from:

            new_casco_vehicle_insurance = TrailerInsurance(
                trailer=trailer,
                type='1',
                from_date = casco_date_from,
                to_date=casco_date_to,
            )
            new_casco_vehicle_insurance.save()

            if casco_contragent:
                try:
                    contragent_insurance = ContragentInsurance.objects.get(title = casco_contragent.upper())
                except ContragentInsurance.DoesNotExist:
                    contragent_insurance = ContragentInsurance(title=casco_contragent.upper())
                    contragent_insurance.save()
                new_casco_vehicle_insurance.contragent =  contragent_insurance
                new_casco_vehicle_insurance.save()
            if owner_contragent:
                try:
                    owner_insurance = OwnerInsurance.objects.get(title = owner_contragent.upper())
                except OwnerInsurance.DoesNotExist:
                    owner_insurance = OwnerInsurance(title=owner_contragent.upper())
                    owner_insurance.save()
                new_casco_vehicle_insurance.owner =  owner_insurance
                new_casco_vehicle_insurance.save()    


        # print(car_number)
        # print(car_title)
        # print(car_year)
        # print(car_vin)
        # print(osago_date_to)
        # print(osago_contragent)
        # print(casco_date_from)
        # print(casco_date_to)
        # print(casco_contragent)
        
        # break