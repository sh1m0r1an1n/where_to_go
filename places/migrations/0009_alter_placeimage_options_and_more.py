# Generated by Django 5.2 on 2025-07-17 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0008_alter_place_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="placeimage",
            options={
                "ordering": ["order"],
                "verbose_name": "Изображение места",
                "verbose_name_plural": "Изображения мест",
            },
        ),
        migrations.RemoveIndex(
            model_name="placeimage",
            name="place_order_idx",
        ),
        migrations.AddIndex(
            model_name="placeimage",
            index=models.Index(fields=["order"], name="place_order_idx"),
        ),
    ]
