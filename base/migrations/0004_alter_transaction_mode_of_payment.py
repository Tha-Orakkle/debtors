# Generated by Django 5.0.6 on 2024-05-14 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_customer_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='mode_of_payment',
            field=models.CharField(choices=[('cash', 'cash'), ('bank_transaction', 'bank_transaction')], max_length=20, null=True),
        ),
    ]
