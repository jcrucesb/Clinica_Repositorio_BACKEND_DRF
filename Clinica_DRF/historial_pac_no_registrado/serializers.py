# Esto debe ir en el serializers.
from historial_pac_no_registrado.models import HistorialPacNoRegistradoModel
from rest_framework import serializers

# Create your models here.
class HistorialPacNoRegistradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPacNoRegistradoModel
        fields = ['id', 'fecha_historial', 'sintoma', 'diagnostico', 'observacion', 'reserva_uuid', 'fk_pac_no_registrado']
    