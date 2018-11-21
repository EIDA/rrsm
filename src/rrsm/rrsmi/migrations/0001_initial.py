# Generated by Django 2.0.4 on 2018-11-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchCombined',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('magnitude_min', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('pga_min', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pga_max', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pgv_min', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pgv_max', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('stat_lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('stat_lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('stat_lon_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('stat_lon_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SearchCustom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, max_length=256)),
                ('date_start', models.DateField(blank=True, default='')),
                ('date_end', models.DateField(blank=True, default='')),
                ('magnitude_min', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('network_code', models.CharField(blank=True, max_length=256)),
                ('station_code', models.CharField(blank=True, max_length=256)),
                ('pga_min', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pga_max', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pgv_min', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pgv_max', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('stat_lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('stat_lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('stat_lon_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('stat_lon_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lon_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lon_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SearchEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, max_length=256)),
                ('date_start', models.DateField(blank=True, default='')),
                ('date_end', models.DateField(blank=True, default='')),
                ('magnitude_min', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('network_code', models.CharField(blank=True, max_length=256)),
                ('station_code', models.CharField(blank=True, max_length=256)),
                ('event_lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lon_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
                ('event_lon_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SearchPeakMotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pga_min', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pga_max', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pgv_min', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('pgv_max', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
