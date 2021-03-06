# Generated by Django 3.2.3 on 2021-05-19 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_auto_20210517_0716"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="follow",
            name="unique_subscription",
        ),
        migrations.RenameField(
            model_name="follow",
            old_name="author",
            new_name="following",
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("user", "following"), name="unique_subscription"
            ),
        ),
    ]
