# Generated by Django 2.2.1 on 2019-06-10 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeaconManager', '0003_layout_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='layout',
            name='length',
            field=models.CharField(default='640', help_text="Layout's length", max_length=10),
        ),
        migrations.AddField(
            model_name='layout',
            name='width',
            field=models.CharField(default='360', help_text="Layout's width)", max_length=10),
        ),
    ]
