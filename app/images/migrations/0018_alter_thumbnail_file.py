# Generated by Django 4.1.3 on 2022-11-21 01:55

from django.db import migrations, models
import images.validators


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0017_alter_thumbnail_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='file',
            field=models.ImageField(upload_to='.', validators=[images.validators.validate_image_extension]),
        ),
    ]
