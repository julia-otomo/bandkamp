from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema


class SongView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Song.objects.filter(album_id=pk)

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        album = get_object_or_404(Album, id=pk)
        serializer.save(album=album)

    @extend_schema(
        operation_id="song_create",
        summary="Create a song data",
        description="Create an album song",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        operation_id="song_get",
        summary="List songs",
        description="List all album songs",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
