# Generated by Django 4.0.4 on 2022-07-06 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_ud_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ud_at',
        ),
    ]
