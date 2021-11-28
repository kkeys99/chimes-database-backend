from django.db import models


class Performer(models.Model):
    name = models.TextField(null=True, blank=True)
    initials = models.TextField(null=True, blank=True)
