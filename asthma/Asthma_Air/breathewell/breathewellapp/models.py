from django.db import models
from django.utils import timezone
#from breathewellapp import admin


# Create your models here.


class Register(models.Model):
    username = models.CharField(max_length=100,null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    confirmpassword = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medicalconditions = models.CharField(max_length=200, null=True, blank=True)
    alertthreshold= models.IntegerField(null=True, blank=True)
    notificationmethod= models.CharField(max_length=100, null=True, blank=True)





class EnvironmentalData(models.Model):
    pm25 = models.FloatField()
    co = models.FloatField()
    nh3 = models.FloatField()
    ch4 = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    recorded_at = models.DateTimeField(default=timezone.now)



class WearableData(models.Model):
    heart_rate = models.IntegerField()
    spo2 = models.IntegerField()
    body_temp = models.FloatField()
    recorded_at = models.DateTimeField(default=timezone.now)


from datetime import datetime
class RiskPrediction(models.Model):
    pm25 = models.FloatField()
    co = models.FloatField()
    heart_rate = models.IntegerField()
    spo2 = models.IntegerField()
    risk_level = models.CharField(max_length=10)
    advisory = models.TextField()
    reading_time = models.DateTimeField(default=datetime.now())





class HistoricalData(models.Model):
    TIMEFRAME_CHOICES = [
        ('24hr', '24 Hours'),
        ('7day', '7 Days'),
        ('30day', '30 Days'),
    ]

    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='historical_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    pm25 = models.FloatField()
    heart_rate = models.IntegerField()

from django.db import models

class SensorData(models.Model):
    value1 = models.FloatField()
    value2 = models.FloatField()
    value3 = models.FloatField()
    value4 = models.FloatField()
    value5 = models.FloatField()
    value6 = models.CharField(max_length=100,blank=True)
    value7 = models.CharField(max_length=100,blank=True)
    reading_time=models.DateTimeField()

    class Meta:
        managed = False  # Django will NOT create/modify table
        db_table = 'sensordata'
from django.db import models

class PollutedData(models.Model):
    place_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField(default=100)  # meters

    def __str__(self):
        return self.place_name
