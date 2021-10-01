from django.http.response import HttpResponse
from django.shortcuts import render

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
				# print(element)
				# Por cada elemento, consultamos la alcaldía de acuerdo a la latitud y longitud
				mayoralty = getMayoraltyInfo(element['position_latitude'], element['position_longitude'])

			return HttpResponse('Datos del metrobus leidos', 200)



# Función para leer la información del punto geográfico y obtener la alcaldía o municipio y actualizar el registro
def getMayoraltyInfo(latitude, longitude):
	# Inicializamos la variable a regresar
	mayoralty = None
	mayoralty_list = []
	mayoralty_rank = []
	# Obtener la info de la api del INEGI
	url_inegi = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/todos/' + str(latitude) + ',' +  str(longitude) + '/150/993701cf-e6bd-48a4-b521-f735c6f9e184'
	# Comprobamos si hubo respuesta exitosa
	info = requests.get(url_inegi)
	# Comprobar si hubo respuesta exitosa
	if (info.status_code == 200):
		# Se parsean los datos de la api de JSON a diccionario
		inegi_data = json.loads(info.text)
		print()
		# Como es un arreglo, recorremos cada elemento
		for element in inegi_data:
			mayoralty_aux = element['Ubicacion'].split(',')[1]
			if mayoralty_aux not in mayoralty_list:
				mayoralty_list.append(mayoralty_aux)
				mayoralty_rank.append(1)
			else:
				pass

		if len(mayoralty_list) == 1:
			mayoralty = mayoralty_list[0]
		else:
			print('tenemos un problema', mayoralty_list)
		
		return mayoralty
	else:
		print('no se pudo leer inegi')



# Función para obtener las unidades disponibles
def getUnitsAvailable(request):
	pass



# Función para obtener el histórico de una unidad
def getUnitRecord(request):
	pass



# Función para obtener las alcaldías Disponibles
def getMayoraltiesAvailable(request):
	pass



# Función para obtener las unidades de una alcaldía
def getUnitsFromMayoralty(request):
	pass