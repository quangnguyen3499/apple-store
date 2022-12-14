# Generated by Django 4.1 on 2022-08-23 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_order_payment_method'),
        ('inventory', '0002_inventory_quantity_alter_stock_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_stock_qty', models.IntegerField(default=0)),
                ('available_stock_qty', models.IntegerField(default=0)),
                ('product', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='store.product')),
            ],
        ),
    ]
