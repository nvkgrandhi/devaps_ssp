from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=30)


# class Tools(models.Model):
#     user = models.OneToOneField(User)
#     tool_name = models.CharField(max_length=50)
#     tool_description = models.CharField(max_length=300)
