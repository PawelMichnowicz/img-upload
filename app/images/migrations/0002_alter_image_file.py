# Generated by Django 4.1.3 on 2022-11-16 19:13

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to=images.models.upload_to),
        ),
    ]
