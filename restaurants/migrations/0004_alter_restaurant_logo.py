# Generated by Django 4.0.2 on 2022-02-28 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_restaurant_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='logo',
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]