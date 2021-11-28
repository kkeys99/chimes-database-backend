from typing import List

from rest_framework import serializers

from api.models import Song
from api.utils import StringListField


class SongSerializer(serializers.ModelSerializer):
    sheets = StringListField(allow_empty=False)
    composers = StringListField(allow_empty=False, required=False, allow_null=True)
    arrangers = StringListField(allow_empty=False, required=False, allow_null=True)
    genres = StringListField(allow_empty=False, required=False, allow_null=True)
    keys = StringListField(allow_empty=False, required=False, allow_null=True)
    time = StringListField(allow_empty=False, required=False, allow_null=True)
    tempos = StringListField(allow_empty=False, required=False, allow_null=True)
    note = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Song
        fields = [
            "id",
            "name",
            "sheets",
            "composers",
            "arrangers",
            "genres",
            "keys",
            "time",
            "tempos",
            "note",
            "dateAdded",
        ]
        read_only_fields = ["id", "dateAdded"]

    def create(self, validated_data):
        song = Song.objects.create(
            name=validated_data["name"], note=validated_data.get("note")
        )

        # handle the tags
        for tagType in [
            "sheets",
            "composers",
            "arrangers",
            "genres",
            "keys",
            "time",
            "tempos",
        ]:
            newTags: List[str] = validated_data.get(tagType)

            # if the user provided a type of tag, we need to associate it with the song
            if newTags:
                setattr(song, tagType, newTags)

        return song
