# Generated by Django 2.2.4 on 2019-09-25 07:54

import datetime
import django.contrib.auth.models
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trelloapp', '0002_auto_20190924_0942'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='board',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='board',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 25, 7, 54, 16, 279398, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 25, 7, 54, 16, 280044, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='trellolist',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 25, 7, 54, 16, 279729, tzinfo=utc)),
        ),
    ]
