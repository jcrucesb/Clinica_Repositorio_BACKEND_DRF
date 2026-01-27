from rest_framework import serializers
from.models import Especialidad
class EspecialidadSerializers(serializers.ModelSerializer):
    nombre_especialidad = serializers.CharField(max_length=250)
    class Meta:
        model = Especialidad
        fields = ["id",'nombre_especialidad', 'valor_especialidad']