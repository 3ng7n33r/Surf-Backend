# Generated by Django 3.1.7 on 2021-04-26 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lat', models.DecimalField(decimal_places=4, max_digits=6)),
                ('lng', models.DecimalField(decimal_places=4, max_digits=7)),
                ('orientation', models.DecimalField(decimal_places=4, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.CharField(choices=[('06:00', '06:00'), ('09:00', '09:00'), ('12:00', '12:00'), ('15:00', '15:00'), ('18:00', '18:00'), ('21:00', '21:00')], max_length=5)),
                ('airTemperature', models.DecimalField(decimal_places=2, max_digits=4)),
                ('cloudCover', models.DecimalField(decimal_places=2, max_digits=5)),
                ('windSpeed', models.DecimalField(decimal_places=2, max_digits=5)),
                ('windDirection', models.DecimalField(decimal_places=4, max_digits=7)),
                ('beach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.beach')),
            ],
        ),
        migrations.CreateModel(
            name='Wave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.CharField(choices=[('06:00', '06:00'), ('09:00', '09:00'), ('12:00', '12:00'), ('15:00', '15:00'), ('18:00', '18:00'), ('21:00', '21:00')], max_length=5)),
                ('waveDirection', models.DecimalField(decimal_places=4, max_digits=7)),
                ('waveHeight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('wavePeriod', models.DecimalField(decimal_places=2, max_digits=5)),
                ('waterTemperature', models.DecimalField(decimal_places=2, max_digits=4)),
                ('beach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.beach')),
            ],
        ),
        migrations.CreateModel(
            name='Tide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.CharField(max_length=5)),
                ('tide', models.CharField(choices=[('low', 'low'), ('high', 'high')], max_length=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('beach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.beach')),
            ],
        ),
    ]
