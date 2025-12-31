"""Backfill `forum_id` for Subforum rows.

For each Subforum with `forum_id` NULL:
- If `parent_forum` is set, copy that id into `forum_id`.
- Otherwise create a new Forum named `migrated_forum_<subforum_id>` and link it.

This migration is reversible as a noop.
"""
from django.db import migrations


def backfill_forum_id(apps, schema_editor):
    Subforum = apps.get_model('db', 'Subforum')
    Forum = apps.get_model('db', 'Forum')

    for s in Subforum.objects.filter(forum_id__isnull=True):
        # Use existing parent_forum when available
        if getattr(s, 'parent_forum_id', None):
            s.forum_id_id = s.parent_forum_id
            s.save(update_fields=['forum_id'])
            continue

        # Otherwise create a new Forum and attach it
        base_name = f"migrated_forum_{str(s.subforum_id)[:8]}"
        name = base_name
        suffix = 1
        # ensure unique forum_name
        while Forum.objects.filter(forum_name=name).exists():
            name = f"{base_name}_{suffix}"
            suffix += 1

        f = Forum.objects.create(
            forum_name=name,
            description=(s.description or ''),
        )

        s.forum_id = f
        s.save(update_fields=['forum_id'])


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0004_subforum_forum_id_alter_forum_forum_name_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_forum_id, migrations.RunPython.noop),
    ]
