# Generated by Django 2.1.15 on 2020-10-02 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0011_auto_20200930_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_track',
            name='cartid',
            field=models.CharField(default=22, max_length=30),
            preserve_default=False,
        ),
    ]