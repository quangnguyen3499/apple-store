# Generated by Django 4.0.6 on 2022-09-08 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_alter_payment_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='total_order',
            new_name='total_remain',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='invoice_url',
        ),
        migrations.AddField(
            model_name='invoice',
            name='currency',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('PARTIALLY_PAID', 'Partially Paid')], default='PENDING', max_length=255),
        ),
    ]
