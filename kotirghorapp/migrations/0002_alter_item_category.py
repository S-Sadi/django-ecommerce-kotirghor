# Generated by Django 4.0.5 on 2022-06-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kotirghorapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('BP', 'Bamboo Products'), ('CP', 'Cane Products'), ('EP', 'Earthenware')], max_length=2),
        ),
    ]
