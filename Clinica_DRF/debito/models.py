from django.db import models

# Create your models here.
class DebitoModel(models.Model):
    debito = models.IntegerField(null=True)
    monto = models.IntegerField(null=True)
    monto_total = models.IntegerField(null=True)
    debito_uuid = models.TextField(max_length=250, null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fk_reserva = models.OneToOneField('reserva.ReservaModel', on_delete=models.SET_NULL, null=True, unique=True)