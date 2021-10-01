from rest_framework import serializers


class AcceptTermsSerializer(serializers.Serializer):
	accept = serializers.BooleanField()

	def validate(self, data):
		if data['accept'] == False:
			raise serializers.ValidationError({'accept': ("Tienes que aceptar los términos y condiciones para continuar.")})
		return data
