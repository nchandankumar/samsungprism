# Generated by Django 4.0.1 on 2022-02-05 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_delete_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='image',
            new_name='cimage',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='cname',
        ),
    ]
