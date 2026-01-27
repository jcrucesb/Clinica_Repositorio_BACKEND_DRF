from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class DoctorModel(models.Model):
    primer_nombre = models.CharField(max_length=250, null=True)
    segundo_nombre = models.CharField(max_length=250, null=True)
    ap_paterno = models.CharField(max_length=250, null=True)
    ap_materno = models.CharField(max_length=250, null=True)
    edad = models.IntegerField(null=True)
    sexo = models.CharField(max_length=1, null=True)
    rut = models.TextField(max_length=250, null=True)
    fono = models.TextField(max_length=250, null=True)
    fk_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor_uuid = models.CharField(max_length=250, null=True)
    # Relación ManyToMany con tabla intermedia, crea una tabla intermedia.
    # RECUERDA, ENTRE RELACIONES DE MUCHOS A MUCHOS, DRF SE ENCARGA DE CREAR UNA TABLA INTERMEDIA.
    # nO ES NECESARIO CREAR LA TABLA INTERMEDIA.
    especialidades = models.ManyToManyField('especialidad.Especialidad')
    doctor_clinica = models.ManyToManyField('comuna_clinica.ComunaClinicaModel')