# Generated by Django 3.1.4 on 2021-01-08 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebapp', '0021_auto_20210108_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyaccounts',
            name='visible',
            field=models.IntegerField(choices=[(0, 'Hidden'), (1, 'Visible')], default=1),
        ),
    ]