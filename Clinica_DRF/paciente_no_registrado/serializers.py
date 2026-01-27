from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import PacienteNoRegisterModel

# Create your models here.
class PacienteNoRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteNoRegisterModel
        fields = ['primer_nombre', 'segundo_nombre', 'ap_materno','ap_paterno','edad', 'sexo', 'rut', 'fono', 'email','paciente_uuid']