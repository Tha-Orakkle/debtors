# Generated by Django 4.2.11 on 2024-05-04 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_transaction_prev_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='prev_amount',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]
