from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import CreditoModel

class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditoModel
        fields = ['id', 'credito', 'fecha_pago', 'credito_uuid','cant_cuotas', 'monto','monto_total', 'monto_cuotas', 'fk_reserva']
        





