# Generated by Django 4.0.1 on 2022-01-17 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_receipt_product_receipt_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='total_price',
            field=models.IntegerField(verbose_name='Сумма'),
        ),
    ]