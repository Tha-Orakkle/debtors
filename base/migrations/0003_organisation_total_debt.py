# Generated by Django 5.1.1 on 2024-10-09 22:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_other_name_alter_user_telephone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='total_debt',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=11),
        ),
    ]
