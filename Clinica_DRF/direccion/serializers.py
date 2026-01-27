from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import DireccionModel

# Create your models here.
class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionModel
        fields = ['id', 'region', 'comuna', 'vivienda','num_vivienda', 'fk_paciente']