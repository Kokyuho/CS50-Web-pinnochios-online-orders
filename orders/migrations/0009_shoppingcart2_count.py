# Generated by Django 3.0.4 on 2020-04-08 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_quantity2_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart2',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
