# Generated by Django 4.2.17 on 2024-12-31 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='monitor',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
