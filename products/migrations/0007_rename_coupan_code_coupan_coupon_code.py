# Generated by Django 4.1.2 on 2022-10-12 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_coupan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupan',
            old_name='coupan_code',
            new_name='coupon_code',
        ),
    ]
