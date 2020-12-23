# Generated by Django 2.1.15 on 2020-09-30 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0006_auto_20200930_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_track',
            name='order_type',
            field=models.CharField(choices=[('abandon order', 'abandon order'), ('normal order', 'normal order'), ('recovered order', 'recovered order'), ('recoverable order', 'recoverable order')], default='normal order', max_length=18),
        ),
    ]