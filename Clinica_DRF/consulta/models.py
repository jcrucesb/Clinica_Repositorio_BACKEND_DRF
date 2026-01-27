from django.db import models
from django.utils.timezone import now

# Create your models here.
class ConsultaModel(models.Model):
    fecha_creacion_consulta = models.DateTimeField(default=now)
    primer_nombre = models.TextField(max_length=250, null=True)
    segundo_nombre = models.TextField(max_length=250, null=True)
    ap_paterno = models.TextField(max_length=100, null=True)
    ap_materno = models.TextField(max_length=100, null=True)
    email = models.TextField(max_length=100, null=True)
    consulta = models.TextField(blank=False, null=True)
    respuesta = models.TextField(blank=False, null=True)
    # 0 = Abierta, 1 = Cerrada
    consulta_cerrada = models.IntegerField(default=0)
    nombre_usuario = models.TextField(max_length=250, null=True)
    fecha_respuesta = models.DateTimeField(default=now, null=True)