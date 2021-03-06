# Generated by Django 3.1.2 on 2020-10-16 20:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aldi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['name'], 'verbose_name': 'Item', 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='itemhistory',
            options={'ordering': ['-datetime_report'], 'verbose_name': 'Item History', 'verbose_name_plural': 'Item History'},
        ),
        migrations.AlterModelOptions(
            name='uom',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='category',
            name='datetime_updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='datetime_updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uom',
            name='datetime_updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(max_length=20, unique=True, verbose_name='SKU'),
        ),
        migrations.AlterField(
            model_name='item',
            name='upc',
            field=models.CharField(max_length=20, unique=True, verbose_name='UPC'),
        ),
        migrations.AlterModelTable(
            name='itemhistory',
            table='item_history',
        ),
    ]
