# Generated by Django 4.0.6 on 2022-10-13 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_account', '0003_cart_coupon'),
        ('products', '0007_rename_coupan_code_coupan_coupon_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Coupan',
            new_name='Coupon',
        ),
    ]
