# Generated by Django 3.2.5 on 2021-08-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210821_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaldoctors',
            name='facebook',
            field=models.URLField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='hospitaldoctors',
            name='instagram',
            field=models.URLField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='hospitaldoctors',
            name='linkedin',
            field=models.URLField(blank=True, default='', max_length=256, null=True),
        ),
    ]