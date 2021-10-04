from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import MetrobusTracking
from .serializers import MayoraltiesAvailableSerializer, UnitRecordsSerializer, UnitsAvailableSerializer

from itertools import groupby
from operator import itemgetter
import json, requests


# Función para leer los datos del metrobus cada hora e insertar los datos seleccionados en el modelo
def getMetrobusInfo(request):
	# Obtener la info de la api del metrobus
	info = requests.get('https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e')
	# Comprobar si hubo respuesta exitosa
	if (info.status_code == 200):
		# Se parsean los datos de la api de JSON a diccionario
		metrobus_data = json.loads(info.text)
		# Se comprueba que se obtiene información de la api
		if metrobus_data['success'] == True:
			# Se extraen los registros en una variable para ser iterada
			metrobus_records = metrobus_data['result']['records']
			# Recorrer los registros obtenidos
			for element in metrobus_records:
				# Por cada elemento, consultamos la alcaldía de acuerdo a la latitud y longitud
				mayoralty_id, mayoralty_name = getMayoraltyInfo(element['position_latitude'], element['position_longitude'])
				if mayoralty_id is None:
					return HttpResponse('No se encontró la alacaldía', 422)
				else:
					# Verificamos si existe el registro en el modelo
					if not MetrobusTracking.objects.filter(
						vehicle_id 			= element['vehicle_id'],
						mayoralty_id 		= mayoralty_id,
						trip_route_id 		= element['trip_route_id'],
						date 				= element['date_updated'],
					).exists():
						# Si no existe, lo insertamos en el modelo
						MetrobusTracking.objects.create(
								date 				= element['date_updated'],
								vehicle_id 			= element['vehicle_id'],
								vehicle_label 		= element['vehicle_label'],
								latitude 			= element['position_latitude'],
								longitude 			= element['position_longitude'],
								geographic_point	= element['geographic_point'],
								mayoralty_id 		= mayoralty_id,
								mayoralty_name 		= mayoralty_name,
								trip_route_id 		= element['trip_route_id'],
							)
			return HttpResponse('Datos del metrobus leidos', 200)



# Función para leer la información del punto geográfico y obtener la alcaldía o municipio y actualizar el registro
def getMayoraltyInfo(latitude, longitude):
	# Código a utilizar se encontró en https://www.it-swarm-es.com/es/python/compruebe-si-el-punto-geografico-esta-dentro-o-fuera-del-poligono-en-python/832662531/
	from shapely.geometry import Point
	from shapely.geometry.polygon import Polygon

	# Inicializamos las variables a regresar
	mayoralty_id = None
	mayoralty_name = None
	# Obtener la info de la api de límites de alcaldía
	mayoralties = requests.get('https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=dbb00cee-3660-43f6-89c2-8beb433292a8')
	# Comprobar si hubo respuesta exitosa
	if (mayoralties.status_code == 200):
		# Se parsean los datos de la api de JSON a diccionario
		mayoralties_data = json.loads(mayoralties.text)
		# Se comprueba que se obtiene información de la api
		if mayoralties_data['success'] == True:
			# Se extraen los registros en una variable para ser iterada
			mayoralties_records = mayoralties_data['result']['records']
			# Recorrer los registros obtenidos
			for element in mayoralties_records:
				# Se parsean los datos del atributo geo_shape
				variable = json.loads(element['geo_shape'])
				# creamos el poligono con el listado de vectores de puntos geográficos
				polygon = Polygon(variable['coordinates'][0])
				# creamos el punto con las coordiadas recibidas
				# dado que los puntos del poligo parecen venir invertidos, 
				# el punto lo armamos con longitud y latitude en vez de latitide-longitude
				point = Point(longitude, latitude)
				# Checamos si el punto se encuentra dentro del poligono
				if point.within(polygon):
					mayoralty_id = element['id']
					mayoralty_name = element['nomgeo']
					break
	
		return mayoralty_id, mayoralty_name



# Función para obtener las unidades disponibles
def getUnitsAvailable(request):
	# Consultamos todos los registros obteniendo las unidades por si id y etiqueta
	units = MetrobusTracking.objects.all().order_by('vehicle_id')
	# Enviamos la consulta al serializer
	serializer = UnitsAvailableSerializer(units, many=True)
	# Regresamos un objeto json con el listado obtenido
	api_object = {
		'name': 'UnitsAvailable',
		'success': True,
		'records': len(serializer.data), 
		'result': serializer.data,
	}
	return JsonResponse(api_object, safe=False)



# Función para obtener el histórico de una unidad
def getUnitRecords(request, unit_id):
	# Consultamos la etiqueta de la unidad
	label = MetrobusTracking.objects.filter(vehicle_id=unit_id).values('vehicle_label').distinct()
	# Consultamos los registros relacionados al ID de una unidad
	records = MetrobusTracking.objects.filter(vehicle_id=unit_id).order_by('-date')
	# Enviamos la consulta al serializer
	serializer = UnitRecordsSerializer(records, many=True)
	# Regresamos un objeto json con el listado obtenido
	api_object = {
		'name': 'UnitRecords',
		'success': True,
		'vehicle_id': unit_id,
		'vehicle_label': label[0]['vehicle_label'],
		'records': len(serializer.data), 
		'result': serializer.data,
	}
	return JsonResponse(api_object, safe=False)



# Función para obtener las alcaldías Disponibles
def getMayoraltiesAvailable(request):
	# Consultamos todos los registros obteniendo las alcaldías
	mayoralties = MetrobusTracking.objects.all().order_by('mayoralty_name').values('mayoralty_id','mayoralty_name').distinct()
	# Enviamos la consulta al serializer
	serializer = MayoraltiesAvailableSerializer(mayoralties, many=True)
	# Regresamos un objeto json con el listado obtenido
	api_object = {
		'name': 'MayoraltiesAvailable',
		'success': True,
		'records': len(serializer.data), 
		'result': serializer.data,
	}
	return JsonResponse(api_object, safe=False)



# Función para obtener las unidades de una alcaldía
def getUnitsFromMayoralty(request, mayoralty_id):
	# Consultamos el nombre de la alcaldía
	name = MetrobusTracking.objects.filter(mayoralty_id=mayoralty_id).values('mayoralty_name').distinct()
	# Consultamos todos los registros de la alcaldía correspondiente
	records = MetrobusTracking.objects.filter(mayoralty_id=mayoralty_id).order_by('vehicle_id').values('vehicle_id','vehicle_label').distinct()
	# Enviamos la consulta al serializer
	serializer = UnitsAvailableSerializer(records, many=True)
	# Regresamos un objeto json con el listado obtenido
	api_object = {
		'name': 'UnitsFromMayoralty',
		'success': True,
		'mayoralty_id': mayoralty_id,
		'mayoralty_name': name[0]['mayoralty_name'],
		'records': len(serializer.data), 
		'result': serializer.data,
	}
	return JsonResponse(api_object, safe=False)
