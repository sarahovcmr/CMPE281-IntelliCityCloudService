from django.db import models
from django.utils import timezone


# Create your models here.
class Device(models.Model):
    station_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=48, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    district = models.IntegerField()
    hourlySpeed = models.CharField(max_length=512, null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'iots'


class User(models.Model):
    email = models.EmailField(unique=True, primary_key=True)
    password = models.CharField(max_length=128)
    firstname = models.CharField(max_length=30, null=True)
    lastname = models.CharField(max_length=30, null=True)
    is_agent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    # Necessary to integrate with Django's authentication system
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.email