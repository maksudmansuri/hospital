# Generated by Django 3.2.5 on 2021-09-30 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_rename_petient_forsome_patient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-created_at']},
        ),
    ]
