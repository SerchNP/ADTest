from rest_framework import serializers

from .models import MetrobusTracking


class UnitsAvailableSerializer(serializers.ModelSerializer):
	class Meta:
		model = MetrobusTracking
		fields = ('vehicle_id', 'vehicle_label')



class UnitRecordsSerializer(serializers.ModelSerializer):
	class Meta:
		model = MetrobusTracking
		fields = ('date', 'geographic_point', 'mayoralty_name')



class MayoraltiesAvailableSerializer(serializers.ModelSerializer):
	class Meta:
		model = MetrobusTracking
		fields = ('mayoralty_id', 'mayoralty_name')
