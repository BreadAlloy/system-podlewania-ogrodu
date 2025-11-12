from django.db import models
from django.contrib.auth.models import User

class Zawor(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.name

