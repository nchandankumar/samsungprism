# Generated by Django 4.0.1 on 2022-03-25 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_comments_complist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='compList',
        ),
        migrations.AddField(
            model_name='comments',
            name='compList',
            field=models.CharField(default='No Comments', max_length=100),
        ),
    ]
