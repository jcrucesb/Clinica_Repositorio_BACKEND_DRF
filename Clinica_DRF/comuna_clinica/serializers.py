from comuna_clinica.models import ComunaClinicaModel
from rest_framework import serializers

class ComunaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComunaClinicaModel
        fields = ['id', 'nombre_clinica', 'comuna_clinica', 'direccion_clinica']