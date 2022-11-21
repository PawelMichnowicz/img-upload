# Generated by Django 4.1.3 on 2022-11-17 21:20

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_image_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='file_50',
        ),
        migrations.AddField(
            model_name='image',
            name='file_200px',
            field=models.ImageField(null=True, upload_to=images.models.upload_to),
        ),
        migrations.AddField(
            model_name='image',
            name='file_400px',
            field=models.ImageField(null=True, upload_to=images.models.upload_to),
        ),
    ]
