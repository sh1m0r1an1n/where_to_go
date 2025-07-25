# Generated by Django 5.2 on 2025-07-15 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0004_alter_placeimage_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="description_long",
            field=models.TextField(blank=True, verbose_name="Подробное описание"),
        ),
        migrations.AlterField(
            model_name="place",
            name="description_short",
            field=models.TextField(blank=True, verbose_name="Краткое описание"),
        ),
    ]
