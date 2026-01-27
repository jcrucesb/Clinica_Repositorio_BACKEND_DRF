from django.contrib.auth.models import Group, User
from usuarios.models import CustomersUsers
from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import PacienteModel

# Create your models here.
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteModel
        fields = ['primer_nombre', 'segundo_nombre', 'edad', 'sexo', 'rut', 'fono','paciente_uuid','fk_user', 'ap_materno','ap_paterno']
    
    # Este método es para realizar la insercción del Paciente al grupo Paciente de forma automatica cuando se ingrese un paciente.
    def create(self, validated_data):
        # Obtener el ID del usuario
        user_id = validated_data.get('fk_user')

        # Recuperar el objeto User desde el ID
        user = CustomersUsers.objects.get(id=user_id.id)

        # Asignar al grupo "Paciente"
        grupo_paciente, creado = Group.objects.get_or_create(name='Paciente')
        user.groups.add(grupo_paciente)

        # Crear el paciente
        paciente = PacienteModel.objects.create(**validated_data)
        return paciente