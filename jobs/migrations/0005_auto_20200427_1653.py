# Generated by Django 3.0.5 on 2020-04-27 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20200427_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='job_title',
            new_name='title',
        ),
    ]
