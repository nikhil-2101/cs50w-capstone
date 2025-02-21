# Generated by Django 5.0.6 on 2024-06-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="interests",
            field=models.CharField(
                blank=True,
                choices=[
                    ("a", "Movie"),
                    ("b", "Drama"),
                    ("c", "Concert"),
                    ("d", "Party"),
                    ("e", "Art"),
                    ("f", "Uncategorized"),
                ],
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="keywords",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_category",
            field=models.CharField(
                choices=[
                    ("a", "Movie"),
                    ("b", "Drama"),
                    ("c", "Concert"),
                    ("d", "Party"),
                    ("e", "Art"),
                    ("f", "Uncategorized"),
                ],
                default="f",
                max_length=1,
            ),
        ),
    ]
