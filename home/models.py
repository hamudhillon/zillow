from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Clans(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    payment = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    roomid = models.CharField(max_length=200,null = True,default = None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



