# Generated by Django 4.0.1 on 2022-02-05 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_photo_description_photo_cname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Images',
        ),
    ]
