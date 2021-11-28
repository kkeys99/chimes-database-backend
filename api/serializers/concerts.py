from rest_framework import serializers

from api.models import Concert, Note, Performance, Performer, Song


class SongSummarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Song
        fields = ["id", "name", "sheets"]
        read_only_fields = ["name", "sheets"]


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = ["initials"]


class PerformanceSerializer(serializers.ModelSerializer):
    performers = PerformerSerializer(many=True, allow_empty=False)
    song = SongSummarySerializer()

    class Meta:
        model = Performance
        fields = ["song", "index", "performers", "request"]


class NoteSerializer(serializers.ModelSerializer):
    author = PerformerSerializer()

    class Meta:
        model = Note
        fields = ["author", "text", "public"]

    def create(self, validated_data):
        validated_data.pop("stupid")


class ConcertSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField()
    concertType = serializers.ChoiceField(
        choices=["morning", "afternoon", "evening", "specialty"],
        source="get_concertType_display",
    )
    performances = PerformanceSerializer(
        many=True, source="performance_set", allow_empty=False
    )
    notes = NoteSerializer(many=True, source="note_set", required=False)

    def create(self, validated_data: dict):
        concertType = Concert.ConcertTypes.labelToCase(
            validated_data.pop("get_concertType_display")
        )
        date = validated_data.pop("date")
        concert = Concert.objects.create(concertType=concertType, date=date)

        self._addPerformances(concert, validated_data.pop("performance_set"))
        self._addNotes(concert, validated_data.pop("note_set", []))
        return concert

    def update(self, instance: Concert, validated_data):
        instance.date = validated_data.get("date", instance.date)
        if "get_concertType_display" in validated_data:
            instance.concertType = Concert.ConcertTypes.labelToCase(
                validated_data["get_concertType_display"]
            )
        if "performance_set" in validated_data:
            for performance in instance.performance_set.all():
                performance.delete()
            self._addPerformances(instance, validated_data["performance_set"])
        if "note_set" in validated_data:
            for note in instance.note_set.all():
                note.delete()
            self._addNotes(instance, validated_data["note_set"])
        instance.save()
        return instance

    @staticmethod
    def _addPerformances(concert, performanceData):
        for performance in performanceData:
            songId = performance.pop("song").pop("id")
            song = Song.objects.get(id=songId)
            performerData = performance.pop("performers")
            newPerformance = Performance.objects.create(
                concert=concert, song=song, **performance
            )
            for performer in performerData:
                performerObj, _ = Performer.objects.get_or_create(
                    initials=performer.pop("initials")
                )
                newPerformance.performers.add(performerObj)

    @staticmethod
    def _addNotes(concert, noteData):
        for note in noteData:
            authorInits = note.pop("author").pop("initials")
            author, _ = Performer.objects.get_or_create(initials=authorInits)
            Note.objects.create(concert=concert, author=author, **note)
