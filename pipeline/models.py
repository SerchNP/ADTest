from django.db import models

# Create your models here.
# Modelo para guardar los datos de las alcaldías y los puntos para formar el poligono
# class Mayoralties(models.Model):
# 	mayoralty_id 		= models.AutoField(primary_key=True)
# 	mayoralty_name 		= models.CharField(max_length=100, null=False)
# 	mayoralty_shape 	= models.TextField(blank=False, null=False)


# Modelo para guardar el historial de las unidades del metrobus junto con su ubicación
class MetrobusTracking(models.Model):
	id 					= models.AutoField(primary_key=True)
	date 				= models.DateTimeField(null=False)
	vehicle_id 			= models.PositiveSmallIntegerField(null=False)
	vehicle_label 		= models.CharField(max_length=10, null=False)
	latitude 			= models.DecimalField(max_digits=18, decimal_places=15, null=False)
	longitude 			= models.DecimalField(max_digits=18, decimal_places=15, null=False)
	geographic_point	= models.CharField(max_length=45, null=False)
	mayoralty_id 		= models.PositiveSmallIntegerField(null=False)
	mayoralty_name 		= models.CharField(max_length=50, null=False)
	trip_route_id 		= models.PositiveSmallIntegerField(null=True)
