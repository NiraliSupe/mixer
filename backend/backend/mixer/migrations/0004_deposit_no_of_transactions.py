# Generated by Django 3.2.12 on 2022-03-16 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixer', '0003_auto_20220316_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='no_of_transactions',
            field=models.IntegerField(default=10, null=True),
        ),
    ]