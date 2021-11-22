from django.db import models


class Tag(models.Model):
    class TagTypes(models.TextChoices):
        SHEET = "SH", "sheet"
        COMPOSER = "CO", "composer"
        ARRANGER = "AR", "arranger"
        GENRE = "GE", "genre"
        KEY = "KE", "key"
        TIME = "TI", "time"
        TEMPO = "TE", "tempo"

    name = models.TextField()
    tagType = models.TextField(choices=TagTypes.choices)

    @property
    def tagTypeLabel(self) -> str:
        return Tag.TagTypes(self.tagType).label


class Song(models.Model):
    name = models.TextField()
    dateAdded = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
