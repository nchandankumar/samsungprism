# Generated by Django 4.0.1 on 2022-02-05 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_cimage_photo_image_photo_cname_photocrop'),
    ]

    operations = [
        migrations.AddField(
            model_name='photocrop',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.photo'),
        ),
    ]
