# Generated by Django 4.0.6 on 2022-08-11 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='status',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='status',
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('DEACTIVATED', 'Deactivated')], db_index=True, default='PENDING', max_length=255),
        ),
    ]