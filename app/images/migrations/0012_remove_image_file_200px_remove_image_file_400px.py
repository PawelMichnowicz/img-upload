# Generated by Django 4.1.3 on 2022-11-20 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0011_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='file_200px',
        ),
        migrations.RemoveField(
            model_name='image',
            name='file_400px',
        ),
    ]
