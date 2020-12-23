# Generated by Django 2.1.15 on 2020-12-03 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0017_auto_20201202_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant_Detail',
            fields=[
                ('m_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('merchant_name', models.CharField(max_length=100)),
                ('tracker_id', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='product_track',
            name='merchant_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
