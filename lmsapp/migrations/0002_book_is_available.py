# Generated by Django 4.2.5 on 2023-09-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
