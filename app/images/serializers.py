import re

from django.core.files import File
from django.urls import reverse
from imagekit import ImageSpec
from imagekit.processors import ResizeToFit
from rest_framework import serializers
from users.models import TierList
from .models import Image, Thumbnail


class ThumbnailGenerator(ImageSpec):
    def __new__(cls, source, height):
        cls.processors = [ResizeToFit(height=height)]
        return super().__new__(cls)

    def __init__(self, source, height):
        super().__init__(source)


class ImageSerializer(serializers.ModelSerializer):
    image_binary = serializers.SerializerMethodField("generate_binary_image")
    binary_expiration_time = serializers.IntegerField(
        max_value=30000, min_value=300, write_only=True, allow_null=True,
    )
    thumbnail_urls = serializers.SerializerMethodField("get_thumbnail_urls")

    class Meta:
        model = Image
        fields = [
            "pk",
            "file",
            "image_binary",
            "binary_expiration_time",
            "thumbnail_urls",
        ]

    def create(self, validated_data):
        validated_data.pop("binary_expiration_time", None)
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def generate_binary_image(self, instance):
        domain = self.context["request"].get_host()
        if (
            hasattr(self, "initial_data")
            and self.initial_data["binary_expiration_time"]
        ):
            if self.context["request"].user.is_access_to_binary_image():
                expiration_time = self.initial_data["binary_expiration_time"]
                return (
                    "http://"
                    + domain
                    + reverse(
                        "images:binary_image", args=[instance.pk, expiration_time]
                    )
                )
            else:
                raise serializers.ValidationError(
                    "You don't have permission to get binary image"
                )
        return None

    def get_thumbnail_urls(self, instance):
        domain = self.context["request"].get_host()
        thumbnails_urls = {}
        thumbnail_sizes = TierList.get_available_sizes(self.context["request"].user)
        for size in thumbnail_sizes:
            thumbnail_file = self.generate_thumbnail(instance.file, size)
            thumbnail_instance = Thumbnail.objects.create_thumbnail(
                instance, thumbnail_file
            )
            thumbnails_urls[size] = "http://" + domain + thumbnail_instance.filepath
        return thumbnails_urls

    @staticmethod
    def generate_thumbnail(source_file, image_size):
        filename, extension = source_file.name.split(".")
        if extension.lower() not in ["png", "jpg", "jpeg"]:
            raise serializers.ValidationError("This is invalid extension of file")
        image_generator = ThumbnailGenerator(source=source_file, height=image_size)
        image = image_generator.generate()
        filename = filename.split("/")[1]
        filename = (
            re.sub("[^A-Za-z0-9]+", "", filename) + f"_{image_size}px" + f".{extension}"
        )
        f = open(filename, "wb+")
        f.write(image.read())
        return File(f)

    def to_representation(self, obj):
        representation = super(ImageSerializer, self).to_representation(obj)
        if not obj.author.is_access_to_original_image():
            representation.pop("file")
        return representation
