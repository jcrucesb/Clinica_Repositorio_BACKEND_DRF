# Esto debe ir en el serializers.
from django.contrib.auth.models import Group, User
from usuarios.models import CustomersUsers
from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import DoctorModel

# Create your models here.
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = ['id', 'primer_nombre', 'segundo_nombre', 'ap_paterno','ap_materno','edad', 'sexo','rut', 'fono','fk_user','doctor_uuid']
    
    # Este método es para realizar la insercción del Doctor al grupo Doctor de forma automatica cuando se ingrese un paciente.
    def create(self, validated_data):
        # Obtener la INSTANCIA del usuario.
        user_id = validated_data.get('fk_user')

        # Recuperar el objeto User desde el ID
        user = CustomersUsers.objects.get(id=user_id.id)

        # Asignar al grupo "Doctor"
        grupo_doctor, creado = Group.objects.get_or_create(name='Doctor')
        user.groups.add(grupo_doctor)

        # Crear el Doctor.
        doctor = DoctorModel.objects.create(**validated_data)
        return doctor
