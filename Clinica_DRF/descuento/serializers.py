from rest_framework import serializers
# Hacemos el llamado a la clase donde agregamos mas cmpos a la tabla User.
from .models import DescuentoModel

# Create your models here.
class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescuentoModel
        fields = ['id', 'fecha_creacion', 'nombre_descuento', 'descripcion', 'cod_descuento','fecha_inicio','fecha_termino', 'descuento']