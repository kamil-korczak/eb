# Generated by Django 3.1.4 on 2020-12-30 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebapp', '0015_auto_20201229_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='status',
            field=models.IntegerField(choices=[(0, 'new'), (1, 'confirmed')], default=0),
        ),
    ]