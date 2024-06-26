# Generated by Django 5.0.4 on 2024-04-15 19:50

import server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0002_alter_category_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True, null=True, upload_to=server.models.category_icon_upload_path
            ),
        ),
    ]
