# Generated by Django 4.1.3 on 2022-11-16 20:23

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_alter_image_file_50'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file_50',
            field=models.FileField(null=True, upload_to=images.models.upload_to),
        ),
    ]
