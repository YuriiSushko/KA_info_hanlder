# Generated by Django 3.1.12 on 2025-05-01 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20250426_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=512),
        ),
    ]
