# Generated by Django 5.0.6 on 2024-06-03 11:43
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    """
    Check Django docs /ref/contrib/postgres/operations/
    """

    dependencies = [
        ("blog", "0004_post_tags"),
    ]

    operations = [
        TrigramExtension(),
    ]
