from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import DescuentoPaciente

# Create your models here.
class DescuentoPacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescuentoPaciente
        fields = ['id', 'total_pagar', 'total_pagar_descuento', 'fecha_utilizacion', 'fk_descuento','fk_paciente']