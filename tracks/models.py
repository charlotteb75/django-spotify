from django.db import models

# Create your models here.
class Track(models.Model ):
    name = models.CharField(max_length=120)
    image = models.ImageField()
    release_date = models.TextField()
    preview = models.TextField()
