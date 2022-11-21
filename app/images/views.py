import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from PIL import Image as PillowImg
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image
from .serializers import ImageSerializer


class ImageApi(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BinaryImageApi(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk, expiration):

        image = get_object_or_404(Image, pk=pk)
        if timezone.now() > (
            image.creation_time + datetime.timedelta(seconds=expiration)
        ):
            content = {"Binary image": "Time expired"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        img = PillowImg.open(image.file)
        thresh = 125
        img = img.convert("L")
        width, height = img.size
        for x in range(width):
            for y in range(height):
                if img.getpixel((x, y)) < thresh:
                    img.putpixel((x, y), 0)
                else:
                    img.putpixel((x, y), 255)

        response = HttpResponse(content_type="image/jpeg")
        img.save(response, "JPEG")
        return response
