# Generated by Django 4.2.7 on 2024-11-18 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="img",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
