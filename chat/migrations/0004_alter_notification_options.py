# Generated by Django 3.2.5 on 2021-10-25 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_notification_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-updated_at']},
        ),
    ]