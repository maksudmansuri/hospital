# Generated by Django 3.2.5 on 2021-08-19 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_hospitaldoctors_ssn_id'),
        ('hospital', '0003_auto_20210818_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalrooms',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2021-08-18 12:36:36.296869'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='department',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hospital.departments'),
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='floor',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='hospital',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals'),
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='room_no',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default='2021-08-18 12:36:36.296869'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RoomOrBadTypeandRates',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(blank=True, choices=[(1, 'A.C'), (2, 'Non-A.C'), (3, 'General')], default='', max_length=50, null=True)),
                ('rooms_price', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.AddField(
            model_name='hospitalrooms',
            name='room_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hospital.roomorbadtypeandrates'),
        ),
    ]