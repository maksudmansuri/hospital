# Generated by Django 3.2.5 on 2021-09-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitals',
            name='profile_pic',
            field=models.FileField(default='', max_length=500, null=True, upload_to='Hospital/profile/images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='hospitals',
            name='registration_proof',
            field=models.FileField(blank=True, default='', max_length=500, null=True, upload_to='hospital/documents/images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='labs',
            name='profile_pic',
            field=models.FileField(default='', max_length=500, null=True, upload_to='hospital/profile/images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='labs',
            name='registration_proof',
            field=models.FileField(blank=True, default='', max_length=500, null=True, upload_to='hospital/documents/images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='patients',
            name='profile_pic',
            field=models.FileField(blank=True, default='', null=True, upload_to='patients/profile/images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='profile_pic',
            field=models.FileField(default='', max_length=500, null=True, upload_to='Pharmacist/profile/images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='registration_proof',
            field=models.FileField(blank=True, default='', max_length=500, null=True, upload_to='Pharmacist/documents/images/%Y/%m/%d/'),
        ),
    ]
