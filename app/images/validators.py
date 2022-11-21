import os
from django.core.exceptions import ValidationError


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in [".jpg", ".png", ".jpeg"]:
        raise ValidationError("Unsupported file extension.")


def validate_file_size(value):
    limit = 25 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Maximum size is equal 25MB")
