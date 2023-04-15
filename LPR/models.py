from django.db import models

# Create your models here.

class StoreImage(models.Model):
    licenseImage = models.ImageField(upload_to='images/')

class DriverInfo(models.Model):
    licenseNo=models.TextField()
    nameOfDriver=models.TextField()
    age=models.IntegerField()
