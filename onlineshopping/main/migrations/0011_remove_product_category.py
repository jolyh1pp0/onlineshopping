# Generated by Django 4.0.1 on 2022-01-17 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_orderitem_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
