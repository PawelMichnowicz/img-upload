from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_image_extension, validate_file_size


def upload_to(instance, filename):
    return "images/{filename}".format(filename=filename)


def upload_to_thumbnails(instance, filename):
    return "thumbnails/{filename}".format(filename=filename)


class Image(models.Model):
    filename = models.CharField(max_length=40)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="images"
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(
        upload_to=upload_to, validators=[validate_image_extension, validate_file_size]
    )


class ThumbnailManager(models.Manager):
    def create_thumbnail(self, image_instance, file):
        thumbnail = self.create(original_image=image_instance, file=file)
        thumbnail.filepath = thumbnail.file.url
        thumbnail.save()
        return thumbnail


class Thumbnail(models.Model):
    original_image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="thumbnails"
    )
    file = models.ImageField(
        upload_to=upload_to_thumbnails, validators=[validate_image_extension]
    )
    filepath = models.CharField(max_length=160)

    objects = ThumbnailManager()
