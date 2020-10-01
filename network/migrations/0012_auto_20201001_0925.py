# Generated by Django 3.1 on 2020-10-01 09:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20200930_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(limit_choices_to={'valid_follow': True}, related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
    ]
