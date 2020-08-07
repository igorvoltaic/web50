# Generated by Django 3.1 on 2020-08-07 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200807_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
