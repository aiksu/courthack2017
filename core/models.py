from django.db import models


class Dictonary(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    description = models.TextField()
