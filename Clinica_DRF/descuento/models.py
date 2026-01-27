# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import MinValueValidator

# Create your models here.
class DescuentoModel(models.Model):
    fecha_creacion = models.DateTimeField(default=now)
    nombre_descuento = models.TextField(max_length=250, null=True)
    descripcion = models.TextField(null=True, blank=True)
    cod_descuento = models.TextField(null=True, blank=True)
    descuento = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    descuento_paciente = models.ManyToManyField(
        'paciente.PacienteModel',
        through='DescuentoPaciente',  # referencia al modelo intermedio
        related_name='descuentos_asignados'
    )
# Creamos la tabla intermedia para agregar algunos campos más.
class DescuentoPaciente(models.Model):
    fk_paciente = models.ForeignKey('paciente.PacienteModel', on_delete=models.CASCADE)
    fk_descuento = models.ForeignKey('DescuentoModel', on_delete=models.CASCADE)
    total_pagar = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    total_pagar_descuento = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    fecha_utilizacion = models.DateField(default=now)