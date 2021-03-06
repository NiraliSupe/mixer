# Generated by Django 3.2.12 on 2022-03-13 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_address', models.TextField()),
                ('requested_amount', models.DecimalField(decimal_places=10, max_digits=15)),
                ('processed_amount', models.DecimalField(decimal_places=10, default=0.0, max_digits=15)),
                ('pooled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DestinationAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_address', models.TextField()),
                ('deposit_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mixer.deposit')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=10, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('destination_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mixer.destinationaddress')),
            ],
        ),
    ]
