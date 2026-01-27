from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import DebitoModel

class DebitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitoModel
        fields = ['id', 'debito', 'monto', 'monto_total','debito_uuid','fecha_pago', 'fk_reserva']
        



