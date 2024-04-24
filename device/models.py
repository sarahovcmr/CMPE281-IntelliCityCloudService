from django.db import models

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