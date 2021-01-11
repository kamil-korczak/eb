# Generated by Django 3.1.4 on 2021-01-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebapp', '0018_auto_20210103_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebaycategories',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='companyaccounts',
            name='company_account',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='ebaycategories',
            name='ebay_category',
            field=models.CharField(max_length=150),
        ),
    ]