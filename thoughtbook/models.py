from django.db import models

# Create your models here.
class thoughts(models.Model):
    thought= models.TextField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=40)
    user = models.CharField(max_length=40)