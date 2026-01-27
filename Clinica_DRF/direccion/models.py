from django.db import models
from django.conf import settings

# Create your models here.
class DireccionModel(models.Model):
    region = models.TextField(max_length=250, null=True)
    comuna = models.TextField(max_length=250, null=True)
    vivienda = models.TextField(max_length=250, null=True)
    num_vivienda = models.TextField(max_length=250, null=True)
    fk_paciente = models.OneToOneField('paciente.PacienteModel', on_delete=models.CASCADE, null=True, unique=True)