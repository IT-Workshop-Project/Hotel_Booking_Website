# Generated by Django 3.1.8 on 2021-06-16 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_hotelmodel_totalprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalamt', models.CharField(max_length=10)),
            ],
        ),
    ]
