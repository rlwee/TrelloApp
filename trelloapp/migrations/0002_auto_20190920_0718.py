# Generated by Django 2.2.4 on 2019-09-20 07:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trelloapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 20, 7, 18, 58, 629851, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='card',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 20, 7, 18, 58, 646477, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='trellolist',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 20, 7, 18, 58, 646139, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='BoardMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trelloapp.Board')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]