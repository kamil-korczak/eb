# Generated by Django 3.1.4 on 2020-12-29 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebapp', '0013_auto_20201228_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='selected',
            field=models.IntegerField(choices=[(0, 'Not selected'), (1, 'Selected')], default=0),
            preserve_default=False,
        ),
    ]
