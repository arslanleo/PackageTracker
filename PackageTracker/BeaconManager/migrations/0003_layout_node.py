# Generated by Django 2.2.1 on 2019-06-10 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BeaconManager', '0002_auto_20190522_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Layout's name (e.g First Floor)", max_length=100)),
                ('image', models.ImageField(help_text='Image of the layout', upload_to='layouts/')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_id', models.CharField(help_text="Node's Unique MAC Address", max_length=12)),
                ('host_address', models.URLField(help_text="Node's host address")),
                ('port', models.CharField(help_text="Node's port number", max_length=4)),
                ('topic', models.CharField(help_text="Node's publish topic (as entered during configuration)", max_length=50)),
                ('user_name', models.CharField(blank=True, help_text="Node's username (optional)", max_length=50, null=True)),
                ('password', models.CharField(blank=True, help_text="Node's password (optional)", max_length=50, null=True)),
                ('location', models.CharField(blank=True, help_text="Node's location (format: x,y)", max_length=7, null=True)),
                ('layout', models.ForeignKey(help_text="Layout's name on which this node is used", null=True, on_delete=django.db.models.deletion.SET_NULL, to='BeaconManager.Layout')),
            ],
            options={
                'ordering': ['layout'],
            },
        ),
    ]
