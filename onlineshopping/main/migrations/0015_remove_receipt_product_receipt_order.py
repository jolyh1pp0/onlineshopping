# Generated by Django 4.0.1 on 2022-01-17 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_product_id_receipt_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='product',
        ),
        migrations.AddField(
            model_name='receipt',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.order'),
        ),
    ]
