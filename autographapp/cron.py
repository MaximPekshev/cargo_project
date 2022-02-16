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

		try:
			autographDay = AutographDailyIndicators.objects.get(vehicle=vehicle, date=date)
		except:
			autographDay = AutographDailyIndicators()
			autographDay.date = date
			autographDay.vehicle = vehicle
			autographDay.driver = vehicle.driver

		autographDay.maxSpeed = Decimal(data.get('maxSpeed')).quantize(Decimal("1.00"))
		autographDay.averageSpeed = Decimal(data.get('averageSpeed')).quantize(Decimal("1.00"))
		autographDay.fuelConsumPerDay = Decimal(data.get('fuelConsumPerDay')).quantize(Decimal("1.00"))
		autographDay.fuelConsumPer100km = Decimal(data.get('fuelConsumPer100km')).quantize(Decimal("1.00"))
		autographDay.rotationMAX = Decimal(data.get('rotationMAX')).quantize(Decimal("1.00"))
		autographDay.parkCount = int(data.get('parkCount'))
		autographDay.totalDistance = Decimal(data.get('totalDistance')).quantize(Decimal("1.00"))

		autographDay.parkCount5MinMore = Decimal(data.get('parkCount5MinMore')).quantize(Decimal("1.00"))
		autographDay.hardBrakingCount = Decimal(data.get('hardBrakingCount')).quantize(Decimal("1.00"))

		autographDay.save()

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

					URL = '{0}GetTrips?session={1}&schemaID={2}&IDs={3}&SD={4}&ED={5}&tripSplitterIndex=-1'.format(
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

							date = yesterday
							parkCount5MinMore = 0
							hardBrakingCount = 0

							totalData = trips[0].get("Total")
							
							if totalData.get("MaxSpeed"):
								maxSpeed = totalData.get("MaxSpeed")
							else:
								maxSpeed = 0

							if totalData.get("AverageSpeed"):
								averageSpeed = totalData.get("AverageSpeed")
							else:
								averageSpeed = 0

							if totalData.get("Engine1FuelConsum"):
								fuelConsumPerDay = totalData.get("Engine1FuelConsum")
							else:
								fuelConsumPerDay = 0

							if totalData.get("Engine1FuelConsum"):
								fuelConsumPerDay = totalData.get("Engine1FuelConsum")
							else:
								fuelConsumPerDay = 0

							if totalData.get("Engine1FuelConsumPer100km"):
								fuelConsumPer100km = totalData.get("Engine1FuelConsumPer100km")
							else:
								fuelConsumPer100km = 0	

							if totalData.get("RotationMAX"):
								rotationMAX = totalData.get("RotationMAX")
							else:
								rotationMAX = 0

							if totalData.get("ParkCount"):
								parkCount = totalData.get("ParkCount")
							else:
								parkCount = 0

							if totalData.get("TotalDistance"):
								totalDistance = totalData.get("TotalDistance")
							else:
								totalDistance = 0	

							stages = trips[0].get("Stages")
							if stages:
								for i in stages:
									if i.get("Name") == "Motion":
										motion = i.get("Items")
								if motion:
									for motion_item in motion:
										if motion_item.get("Caption") == "Остановка":
											totalParkDuration = datetime.datetime.strptime(motion_item.get("Values")[12], '%H:%M:%S').time()
											if totalParkDuration > datetime.time(0, 5, 0):
												parkCount5MinMore += 1


							request_context = {
								'maxSpeed' : maxSpeed,
								'averageSpeed' : averageSpeed,
								'fuelConsumPerDay' : fuelConsumPerDay,
								'fuelConsumPer100km' : fuelConsumPer100km,
								'rotationMAX' : rotationMAX,
								'parkCount' : parkCount,
								'totalDistance' : totalDistance,
								'parkCount5MinMore' : parkCount5MinMore,
								'hardBrakingCount' : hardBrakingCount,
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