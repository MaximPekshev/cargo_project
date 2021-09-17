import xlrd
from cargoapp.models import City

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