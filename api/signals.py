from django.db.models.signals import pre_delete
from django.dispatch import receiver

from api.models import Song


@receiver(pre_delete, sender=Song)
def pre_delete_song(sender, instance: Song, **kwargs):
    # If the song we are about to delete is the last one associated with a tag,
    # then delete the tag entirely
    for tag in instance.tags.all():
        if tag.song_set.count() == 1:
            tag.delete()
