# Generated by Django 4.0.1 on 2022-01-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(upload_to='', verbose_name='Фотография'),
        ),
    ]
