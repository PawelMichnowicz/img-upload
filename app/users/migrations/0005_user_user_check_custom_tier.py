# Generated by Django 4.1.3 on 2022-11-21 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_binary_file_available_tier_binary_file_access_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('custom_tier__isnull', False), ('tier', 'CUSTOM')), models.Q(('custom_tier__isnull', True), ('tier', 'BASIC')), models.Q(('custom_tier__isnull', True), ('tier', 'PREMIUM')), models.Q(('custom_tier__isnull', True), ('tier', 'ENTERPRISE')), _connector='OR'), name='user_check_custom_tier'),
        ),
    ]
