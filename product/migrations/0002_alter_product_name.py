# Generated by Django 5.1.1 on 2024-09-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
