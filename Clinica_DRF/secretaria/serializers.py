# Esto debe ir en el serializers.
from django.contrib.auth.models import Group, User
from usuarios.models import CustomersUsers
from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import SecretariaModel

# Create your models here.
class SecretariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretariaModel
        fields = ['id', 'primer_nombre', 'segundo_nombre', 'ap_paterno', 'ap_materno', 'edad', 'sexo', 'rut', 'fono','secretaria_uuid','fk_user']
    
    # Este método es para realizar la insercción del Paciente al grupo Paciente de forma automatica cuando se ingrese un paciente.
    def create(self, validated_data):
        # Obtener el ID del usuario
        user_id = validated_data.get('fk_user')

        # Recuperar el objeto User desde el ID
        user = CustomersUsers.objects.get(id=user_id.id)

        # Asignar al grupo "Paciente"
        grupo_secreatia, creado = Group.objects.get_or_create(name='Secretaria')
        user.groups.add(grupo_secreatia)

        # Crear el paciente
        secretaria = SecretariaModel.objects.create(**validated_data)
        return secretaria
 
    