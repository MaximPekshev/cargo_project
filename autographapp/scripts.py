from cargoapp.models import Vehicle
from autographapp.models import AutographDailyIndicators
from decouple import config
import requests
import datetime
from decimal import Decimal

def autographAuth():

	login = config('AUTOGRAPH_LOGIN')
	password = config('AUTOGRAPH_PASSWORD')
	autograph_path = config('AUTOGRAPH_BASE_PATH')
	
	authURL = '{}Login?UserName={}&Password={}'.format(autograph_path, login, password)
	answer = requests.get(authURL)
	if answer.status_code == 200:
		return answer.text
	else:
		return None

def enumDevices(session):

	autograph_path = config('AUTOGRAPH_BASE_PATH')
	schemaID = config('AUTOGRAPH_SCHEME')
	URL = '{0}EnumDevices?session={1}&schemaID={2}'.format(autograph_path, session, schemaID)
	answer = requests.get(URL)

	response = answer.json()
	response_vehicles = response.get('Items')
	return response_vehicles

def createAutographDay(data, date, serial):
	try:
		vehicle = Vehicle.objects.get(nav_id=serial)
	except:
		vehicle = None

	if vehicle:

		newAutographDay = AutographDailyIndicators()
		newAutographDay.date = date
		newAutographDay.vehicle = vehicle
		newAutographDay.driver = vehicle.driver

		newAutographDay.maxSpeed = Decimal(data.get('MaxSpeed')).quantize(Decimal("1.00"))
		newAutographDay.averageSpeed = Decimal(data.get('AverageSpeed')).quantize(Decimal("1.00"))

		newAutographDay.fuelConsumPerDay = Decimal(data.get('AverageSpeed')).quantize(Decimal("1.00"))
		newAutographDay.fuelConsumPer100km = Decimal(data.get('AverageSpeed')).quantize(Decimal("1.00"))
		newAutographDay.rotationMAX = Decimal(data.get('RotationMAX')).quantize(Decimal("1.00"))
		newAutographDay.parkCount = int(data.get('ParkCount'))
		newAutographDay.totalDistance = Decimal(data.get('TotalDistance')).quantize(Decimal("1.00"))
		
		newAutographDay.save()

def getRequest(url):

	answer = requests.get(url)

	if answer:
		return answer
	else:
		return None	

def uploadAutographDailyIndicators():

	session = autographAuth()

	if session:

		response_vehicles = enumDevices(session)

		for vehicle in Vehicle.objects.all():
			if vehicle.nav_id:
				vehicleID = None
				for i in response_vehicles:
					if str(i.get('Serial')) == vehicle.nav_id:
						vehicleID = i.get('ID')
						break
				if vehicleID:
					autograph_path = config('AUTOGRAPH_BASE_PATH')
					schemaID = config('AUTOGRAPH_SCHEME')
					yesterday = datetime.datetime.now() -  datetime.timedelta(days=1)
					dateTimeFirst = yesterday.strftime("%Y%m%d")
					dateTimeLast = dateTimeFirst + '-2359'

					URL = '{0}GetTrips?session={1}&schemaID={2}&IDs={3}&SD={4}&ED={5}&tripSplitterIndex=0'.format(
						autograph_path, session, schemaID, vehicleID, dateTimeFirst, dateTimeLast)

					answer = getRequest(URL)
					if answer:
						response = answer.json()
						data = response.get(vehicleID)
						trips = data.get('Trips')
						if trips:
							trips = trips[0]
							createAutographDay(trips.get('Total'), yesterday, data.get('Serial'))
						else:
							pass
					else:
						pass		
				else:
					pass
					# print('No vehicleID')	
		


# from autographapp.scripts import uploadAutographDailyIndicators