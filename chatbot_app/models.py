from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subject(models.Model):
    name=models.CharField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    score=models.IntegerField()



