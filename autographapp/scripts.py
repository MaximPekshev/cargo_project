from django.http import request
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

	try:
		answer = requests.get(URL)
	except:
		answer = None	

	if answer:
		response = answer.json()
		response_vehicles = response.get('Items')
		return response_vehicles
	else:
		return None	

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

		newAutographDay.maxSpeed = Decimal(data.get('maxSpeed')).quantize(Decimal("1.00"))
		newAutographDay.averageSpeed = Decimal(data.get('averageSpeed')).quantize(Decimal("1.00"))
		newAutographDay.fuelConsumPerDay = Decimal(data.get('fuelConsumPerDay')).quantize(Decimal("1.00"))
		newAutographDay.fuelConsumPer100km = Decimal(data.get('fuelConsumPer100km')).quantize(Decimal("1.00"))
		newAutographDay.rotationMAX = Decimal(data.get('rotationMAX')).quantize(Decimal("1.00"))
		newAutographDay.parkCount = int(data.get('parkCount'))
		newAutographDay.totalDistance = Decimal(data.get('totalDistance')).quantize(Decimal("1.00"))
		
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
					dateTimeFirst = yesterday.strftime("%Y%m%d") + '-0300'
					dateTimeLast = datetime.datetime.now().strftime("%Y%m%d") + '-0259'
					# yesterday = datetime.datetime.strptime('20220124', "%Y%m%d")
					# dateTimeFirst = '20220124-0300'
					# dateTimeLast = '20220125-0259'

					URL = '{0}GetTrips?session={1}&schemaID={2}&IDs={3}&SD={4}&ED={5}&tripSplitterIndex=0'.format(
						autograph_path, session, schemaID, vehicleID, dateTimeFirst, dateTimeLast)

					try:
						answer = getRequest(URL)
					except:
						answer = None	

					if answer:

						response = answer.json()
						data = response.get(vehicleID)
						trips = data.get('Trips')
						if trips:

							trips_count = 0
							date = yesterday
							maxSpeed = 0
							averageSpeed = 0
							fuelConsumPerDay = 0
							fuelConsumPer100km = 0
							rotationMAX = 0
							parkCount = 0
							parkCount5MinMore = 0
							hardBrakingCount = 0
							totalDistance = 0

							for item in trips:
								totalData = item.get("Total")

								request_maxSpeed = totalData.get("MaxSpeed")
								if request_maxSpeed:
									if request_maxSpeed > maxSpeed:
										maxSpeed = request_maxSpeed

								request_averageSpeed = totalData.get("AverageSpeed")
								if request_averageSpeed:
									averageSpeed += request_averageSpeed

								request_fuelConsumPerDay = totalData.get("Engine1FuelConsum")
								if request_fuelConsumPerDay:
									fuelConsumPerDay += request_fuelConsumPerDay

								request_fuelConsumPer100km = totalData.get("Engine1FuelConsumPer100km")
								if request_fuelConsumPer100km:
									fuelConsumPer100km += request_fuelConsumPer100km

								request_rotationMAX = totalData.get("RotationMAX")
								if request_rotationMAX:
									if request_rotationMAX > rotationMAX:
										rotationMAX = request_rotationMAX

								request_parkCount = totalData.get("ParkCount")
								if request_parkCount:
									parkCount += request_parkCount

								request_totalDistance = totalData.get("TotalDistance")
								if request_totalDistance:
									totalDistance += request_totalDistance

								trips_count += 1

							request_context = {
								'maxSpeed' : maxSpeed,
								'averageSpeed' : averageSpeed/trips_count,
								'fuelConsumPerDay' : fuelConsumPerDay,
								'fuelConsumPer100km' : fuelConsumPer100km/trips_count,
								'rotationMAX' : rotationMAX,
								'parkCount' : parkCount,
								'totalDistance' : totalDistance,
							}	
							createAutographDay(request_context, date, data.get('Serial'))	
						else:
							pass
					else:
						pass		
				else:
					pass
					# print('No vehicleID')	
		


# from autographapp.scripts import uploadAutographDailyIndicators