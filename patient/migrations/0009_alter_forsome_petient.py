# Generated by Django 3.2.5 on 2021-09-30 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210930_2053'),
        ('patient', '0008_auto_20210930_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forsome',
            name='petient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patients'),
        ),
    ]