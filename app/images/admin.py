from django.contrib import admin

from .models import Image, Thumbnail


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["pk", "author", "file"]
    fieldsets = ((None, {"fields": ("file", "author")}),)


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ["pk", "file", "filepath"]
