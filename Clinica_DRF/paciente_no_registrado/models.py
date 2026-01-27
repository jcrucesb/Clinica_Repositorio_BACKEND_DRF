from django.db import models
from django.conf import settings
#
class PacienteNoRegisterModel(models.Model):
    primer_nombre = models.CharField(max_length=250, null=True)
    segundo_nombre = models.CharField(max_length=250, null=True)
    ap_paterno = models.CharField(max_length=250, null=True)
    ap_materno = models.CharField(max_length=250, null=True)
    edad = models.IntegerField(null=True)
    sexo = models.CharField(max_length=1, null=True)
    rut = models.TextField(max_length=250, null=True)
    fono = models.TextField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    paciente_uuid = models.CharField(max_length=250, null=True)