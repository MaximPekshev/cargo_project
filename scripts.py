import xlrd
from cargoapp.models import City, Vehicle

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
                