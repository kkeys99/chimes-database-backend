from rest_framework import serializers

from api.models import Song
from api.utils import StringListField


class SongSerializer(serializers.ModelSerializer):
    sheets = StringListField(allow_empty=False)
    composers = StringListField(required=False)
    arrangers = StringListField(required=False)
    genres = StringListField(required=False)
    keys = StringListField(required=False)
    time = StringListField(required=False)
    tempos = StringListField(required=False)
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
        song = Song.objects.create()

        editableFields = [
            "name",
            "sheets",
            "composers",
            "arrangers",
            "genres",
            "keys",
            "time",
            "tempos",
            "note",
        ]

        for field in editableFields:
            newVal = validated_data.get(field)
            if newVal:
                setattr(song, field, newVal)

        song.save()
        return song
