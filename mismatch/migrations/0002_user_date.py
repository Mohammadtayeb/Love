# Generated by Django 3.2.2 on 2022-12-20 16:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mismatch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
