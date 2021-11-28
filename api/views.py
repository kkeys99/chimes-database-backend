from rest_framework import viewsets

from api.models import Concert, Song
from api.serializers import ConcertSerializer, SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class ConcertViewSet(viewsets.ModelViewSet):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
