# Generated by Django 4.0.6 on 2022-08-29 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
