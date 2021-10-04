from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	# URL para leer los datos del metrobus
	path('pipeline/metrobus/consultar', 			views.getMetrobusInfo, 					name='metrobus-info'),
	
	# URL API Obtener una lista de unidades disponibles
	path('api/units_available',						views.getUnitsAvailable,				name='units-available'),
	# URL API Consultar los el historial de ubicaciones/fechas de una unidad dado su ID
	path('api/unit_records/<int:unit_id>', 			views.getUnitRecords,					name='unit-records'),
	# URL API Obtener una lista de alcaldías disponibles
	path('api/mayoralties_available',				views.getMayoraltiesAvailable,			name='mayoralties-available'),
	# URL API Obtener una lista de unidades que hayan estado dentro de una alcaldía
	path('api/mayoralty_units/<int:mayoralty_id>', 	views.getUnitsFromMayoralty,			name='units-from-mayoralty'),
]
