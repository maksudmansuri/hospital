# Generated by Django 3.2.5 on 2021-09-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]