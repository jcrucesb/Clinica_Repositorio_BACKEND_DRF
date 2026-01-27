# Create your models here.
from django.db import models
from paciente.models import PacienteModel
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import MinValueValidator
# Create your models here.
class HistorialClinicoModel(models.Model):
    fk_paciente = models.ForeignKey(PacienteModel, on_delete=models.CASCADE)
    fecha_creacion_historial = models.DateTimeField(default=now)
    diagnostico = models.TextField(null=True)
    sintoma = models.CharField(null=True, max_length=200)
    observacion = models.TextField(null=True)
    reserva_uuid = models.CharField(max_length=250, null=True)