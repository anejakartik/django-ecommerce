# Generated by Django 2.2.4 on 2020-08-08 14:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_product_track_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_track',
            old_name='category',
            new_name='product_category',
        ),
        migrations.RenameField(
            model_name='product_track',
            old_name='name',
            new_name='product_name',
        ),
        migrations.RenameField(
            model_name='product_track',
            old_name='price',
            new_name='product_price',
        ),
        migrations.RenameField(
            model_name='product_track',
            old_name='stock_no',
            new_name='sku_id',
        ),
        migrations.AddField(
            model_name='product_track',
            name='added_to_cart',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product_track',
            name='checkout_initiated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product_track',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product_track',
            name='order_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product_track',
            name='product_viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product_track',
            name='user_email',
            field=models.CharField(default='kartik@gmail.com', max_length=100),
            preserve_default=False,
        ),
    ]
