# Generated by Django 3.0.4 on 2020-04-12 11:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0011_shoppingcart2_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart2',
            name='user',
        ),
        migrations.AddField(
            model_name='shoppingcart2',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
