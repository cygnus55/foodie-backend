# Generated by Django 4.0.2 on 2022-03-22 14:38

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foods', '0005_alter_food_image'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_location', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=3)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='customers.customer')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='foods.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
            options={
                'unique_together': {('order', 'food')},
            },
        ),
    ]