from django.db import models

from api.models import Concert, Performer, Song


class Performance(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    performers = models.ManyToManyField(Performer)
    request = models.BooleanField(default=False)
