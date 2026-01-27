from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomersUsers(AbstractUser):
    # Lo dejamos en None para no usar estos campos.
    first_name = None
    last_name = None
    edad = None
    password = models.CharField(max_length=255, null=True)
    usuario_uuid = models.CharField(max_length=250, null=True)