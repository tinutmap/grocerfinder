# Generated by Django 3.1.2 on 2020-10-16 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('sku', models.CharField(max_length=20, unique=True)),
                ('upc', models.CharField(max_length=20, unique=True)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('pack_qty', models.DecimalField(decimal_places=4, max_digits=20)),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='aldi.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Uom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ItemHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('datetime_report', models.DateTimeField(auto_now_add=True, verbose_name='Report Time')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aldi.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='uom',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='aldi.uom', verbose_name='unit of measurement'),
        ),
    ]
