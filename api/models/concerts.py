from django.db import models

from api.models import Performer


class Concert(models.Model):
    class ConcertTypes(models.TextChoices):
        MORNING = "MO", "morning"
        AFTERNOON = "AF", "afternoon"
        EVENING = "EV", "evening"
        SPECIALTY = "SP", "specialty"

        @classmethod
        def labelToCase(cls, label: str):
            for val, lab in cls.choices:
                if lab == label:
                    return cls(val)

    date = models.DateTimeField()
    concertType = models.TextField(choices=ConcertTypes.choices)


class Note(models.Model):
    author = models.ForeignKey(Performer, on_delete=models.CASCADE)
    text = models.TextField()
    public = models.BooleanField(default=False)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
