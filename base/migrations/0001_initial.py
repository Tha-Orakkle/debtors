# Generated by Django 4.2.11 on 2024-04-18 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('payment', 'payment'), ('new_transaction', 'new_transaction')], max_length=16)),
                ('prev_amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('new_amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=11)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=11)),
                ('date_of_payment', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.TextField()),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.organisation'),
        ),
    ]