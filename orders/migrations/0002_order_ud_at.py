# Generated by Django 4.0.4 on 2022-07-06 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ud_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
