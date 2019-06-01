# Generated by Django 2.2.1 on 2019-05-22 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagID', models.CharField(help_text="Tag's Unique MAC Address", max_length=12)),
                ('name', models.CharField(help_text="Tag's given name", max_length=200)),
                ('description', models.CharField(help_text='Description of objects associated with this Tag', max_length=200)),
                ('status', models.CharField(choices=[('p', 'Pending'), ('r', 'Received'), ('s', 'Sent')], default='p', help_text="Tag's status", max_length=1)),
                ('location', models.CharField(help_text="Tag's location", max_length=200)),
            ],
            options={
                'ordering': ['status'],
            },
        ),
    ]
