# Generated by Django 4.1.3 on 2022-11-16 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_alter_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file_50',
            field=models.URLField(default='www.cos.pl', max_length=50),
            preserve_default=False,
        ),
    ]
