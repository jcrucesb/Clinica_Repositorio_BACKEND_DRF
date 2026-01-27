from django.db import models

# Create your models here.
class CreditoModel(models.Model):
    credito = models.IntegerField(null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    credito_uuid = models.CharField(max_length=255, null=True)
    monto = models.IntegerField(null=True)
    cant_cuotas = models.IntegerField(null=True)
    monto_total = models.IntegerField(null=True)
    monto_cuotas = models.IntegerField(null=True)
    fk_reserva = models.OneToOneField('reserva.ReservaModel', on_delete=models.SET_NULL, null=True, unique=True)