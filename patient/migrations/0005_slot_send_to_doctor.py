# Generated by Django 3.2.5 on 2021-09-29 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20210929_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='send_to_doctor',
            field=models.BooleanField(default=False),
        ),
    ]