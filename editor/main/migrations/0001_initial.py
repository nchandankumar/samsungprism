# Generated by Django 4.0.1 on 2022-01-31 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('imgid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('img1', models.ImageField(null=True, upload_to='images')),
                ('img2', models.ImageField(null=True, upload_to='images')),
                ('img3', models.ImageField(null=True, upload_to='images')),
            ],
        ),
    ]
