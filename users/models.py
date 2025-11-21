from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"
