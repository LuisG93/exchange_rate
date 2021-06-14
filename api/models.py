from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Exchange(models.Model):
    ORIGIN = (
        ('D', 'Diario'),
        ('F', 'Fixer'),
        ('B', 'Banxico'),
    )
    origin = models.CharField(max_length=1, choices=ORIGIN)
    value = models.FloatField()
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)



class UserAccess(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_access')
