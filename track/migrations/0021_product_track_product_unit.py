# Generated by Django 2.1.15 on 2020-12-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0020_auto_20201204_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_track',
            name='product_unit',
            field=models.PositiveIntegerField(default=1),
        ),
    ]