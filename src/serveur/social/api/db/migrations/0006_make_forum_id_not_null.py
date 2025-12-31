"""Make Subforum.forum_id non-nullable.

This migration assumes the data migration 0005 ensured no NULL values remain.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0005_backfill_forum_id_create_forums"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subforum",
            name="forum_id",
            field=models.ForeignKey(
                to="db.forum",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subforums_in_forum",
                null=False,
                blank=False,
            ),
        ),
    ]
