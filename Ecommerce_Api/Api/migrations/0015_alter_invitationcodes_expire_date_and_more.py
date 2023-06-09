# Generated by Django 4.1.7 on 2023-04-26 00:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0014_rename_category_id_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationcodes',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 3, 0, 40, 48, 121493, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='invitationcodes',
            name='invitationCodes',
            field=models.CharField(default='ThjQ87JWoO8NKFh', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='dateReleased',
            field=models.DateField(),
        ),
    ]
