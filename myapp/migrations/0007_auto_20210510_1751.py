# Generated by Django 3.1.5 on 2021-05-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210510_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.IntegerField(),
        ),
    ]
