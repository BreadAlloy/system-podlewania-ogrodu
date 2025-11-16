from django.db import models
from django.contrib.auth.models import User

class Zawor(models.Model):
    # name = models.CharField(max_length=50)
    real_id = models.IntegerField(default=0)
    #pin = models.IntegerField(default=None)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.real_id}: status - {self.status}"

