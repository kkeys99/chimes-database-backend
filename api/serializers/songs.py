from collections import defaultdict
from typing import List

from rest_framework import serializers

from api.models import Song, Tag
from api.utils import StringListField


class SongSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    sheet = StringListField(allow_empty=False)
    composer = StringListField(allow_empty=False, required=False, allow_null=True)
    arranger = StringListField(allow_empty=False, required=False, allow_null=True)
    genre = StringListField(allow_empty=False, required=False, allow_null=True)
    key = StringListField(allow_empty=False, required=False, allow_null=True)
    time = StringListField(allow_empty=False, required=False, allow_null=True)
    tempo = StringListField(allow_empty=False, required=False, allow_null=True)
    dateAdded = serializers.DateTimeField(read_only=True)
    note = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data: dict) -> Song:
        song = Song.objects.create(
            name=validated_data["name"], note=validated_data.get("note")
        )

        # handle the tags
        for tagType in Tag.TagTypes:
            label: str = tagType.label
            tagList: List[str] = validated_data.get(label)

            # if the user provided a type of tag, we need to associate it with the song
            if tagList:
                for name in tagList:
                    matchedTag, _ = Tag.objects.get_or_create(
                        name=name, tagType=tagType
                    )
                    song.tags.add(matchedTag)
        return song

    def update(self, instance: Song, validated_data: dict) -> Song:
        # update the name and note if it was provided, otherwise they should stay the same
        if "name" in validated_data:
            instance.name = validated_data["name"]
        if "note" in validated_data:
            instance.note = validated_data["note"]

        # now handle the other tags
        for tagType in Tag.TagTypes:
            label: str = tagType.label
            newTagNames: List[str] = validated_data.get(label)

            # if the user provided null as the value for a tag, make sure we delete all the current tags
            if newTagNames is None and label in validated_data:
                newTagNames = []

            # if the user provided a field, we need to find out how to update the tags
            if newTagNames is not None:
                oldTags = Tag.objects.filter(tagType=tagType)
                oldTagNames = oldTags.values_list("name")

                # if the user didn't provide an old tag in the list of new tags, remove it
                tagsToRemove = [tag for tag in oldTags if tag.name not in newTagNames]

                # if the user provided a tag in the list that's not already a tag, we need to add it
                tagNamesToAdd = [
                    tagName for tagName in newTagNames if tagName not in oldTagNames
                ]

                # if the user provided a tag that IS already a tag, the work is done

                # remove the tag from the song, and delete it if there are no more songs associated with it
                for tag in tagsToRemove:
                    instance.tags.remove(tag)
                    if tag.song_set.count() == 0:
                        tag.delete()

                # if the tag already exists, just add it to the relationship. Make a new one if it doesn't exist
                for newTagName in tagNamesToAdd:
                    newTag, _ = Tag.objects.get_or_create(
                        name=newTagName, tagType=tagType
                    )
                    instance.tags.add(newTag)
        return instance

    def to_representation(self, instance: Song):
        baseFields = [
            ("id", instance.id),
            ("name", instance.name),
            ("dateAdded", instance.dateAdded),
            ("note", instance.note),
        ]
        baseDict = {name: val for name, val in baseFields if val is not None}

        tags = instance.tags.all()
        tagDict = defaultdict(list)
        for tag in tags:
            tagDict[tag.tagTypeLabel].append(tag.name)
        return {
            **baseDict,
            **tagDict,
        }
