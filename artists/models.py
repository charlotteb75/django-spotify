from django.db import models

# Create your models here.
class Artist(models.Model ):
    name = models.CharField(max_length=120)
    #description = models.TextField(blank=True, null=True)
    genres = models.TextField()
    popularity = models.IntegerField()
    #albums = models.TextField(blank=True, null=False)
    image = models.ImageField()
    followers = models.IntegerField()
    id_artist = models.TextField()
