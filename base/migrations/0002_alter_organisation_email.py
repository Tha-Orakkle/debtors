# Generated by Django 5.0.6 on 2024-05-13 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
