# Generated by Django 4.0.1 on 2022-01-16 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_order_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category'),
        ),
    ]