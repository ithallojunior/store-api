# Generated by Django 3.1.2 on 2020-10-27 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.products'),
        ),
    ]
