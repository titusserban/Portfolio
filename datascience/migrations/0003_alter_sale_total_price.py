# Generated by Django 4.0.1 on 2022-02-15 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datascience', '0002_csv_position_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
