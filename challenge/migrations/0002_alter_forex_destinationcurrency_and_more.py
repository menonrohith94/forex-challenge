# Generated by Django 4.1 on 2022-08-10 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forex',
            name='DestinationCurrency',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='forex',
            name='SourceCurrency',
            field=models.TextField(default='', max_length=255),
        ),
    ]
