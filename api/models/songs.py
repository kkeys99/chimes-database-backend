from typing import Dict, List, Optional

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


def addTagProperties(namesAndTypes: Dict[str, Tag.TagTypes]):
    def setProperties(cls):
        for name, tagType in namesAndTypes.items():

            def getter(self, tagType=tagType):
                return self._groupTags(tagType)

            def setter(self, newTags, tagType=tagType):
                return self._updateTagGroup(newTags, tagType)

            prop = property(getter, setter)
            setattr(cls, name, prop)
        return cls

    return setProperties


propertyNamesWithTypes = {
    "sheets": Tag.TagTypes.SHEET,
    "composers": Tag.TagTypes.COMPOSER,
    "arrangers": Tag.TagTypes.ARRANGER,
    "genres": Tag.TagTypes.GENRE,
    "keys": Tag.TagTypes.KEY,
    "time": Tag.TagTypes.TIME,
    "tempos": Tag.TagTypes.TEMPO,
}


@addTagProperties(propertyNamesWithTypes)
class Song(models.Model):
    name = models.TextField()
    dateAdded = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def _groupTags(self, tagType: Tag.TagTypes):
        return (
            self.tags.filter(tagType=tagType)
            .order_by("name")
            .values_list("name", flat=True)
        )

    def _updateTagGroup(self, newTagNames: Optional[List[str]], tagType: Tag.TagTypes):
        oldTags = self.tags.filter(tagType=tagType)

        # clear the old tags from the relationship
        for tag in oldTags:
            self.tags.remove(tag)

        # create a new tag if needed, and add all the new tags to the relationship
        if newTagNames:
            for newName in newTagNames:
                newTag, _ = Tag.objects.get_or_create(name=newName, tagType=tagType)
                self.tags.add(newTag)

        # delete any tags that are now orphaned as a result of this operation
        for tag in oldTags:
            if tag.song_set.count() == 0:
                tag.delete()
