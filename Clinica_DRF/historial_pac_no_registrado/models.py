# Create your models here.
from paciente_no_registrado.models import PacienteNoRegisterModel
from django.db import models
from django.conf import settings

class HistorialPacNoRegistradoModel(models.Model):
    fecha_historial = models.DateField()
    sintoma = models.CharField(max_length=250, null=True)
    diagnostico = models.TextField(null=True)
    observacion = models.TextField(null=True)
    reserva_uuid = models.CharField(max_length=250, null=True)
    fk_pac_no_registrado = models.OneToOneField(
    PacienteNoRegisterModel,
    on_delete=models.CASCADE,
    related_name='paciente_no_registrado'
)