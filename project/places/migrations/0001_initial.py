# Generated by Django 3.2.25 on 2024-09-18 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lng', models.FloatField()),
                ('lat', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinal_number', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description_short', models.CharField(max_length=200)),
                ('description_long', models.TextField()),
                ('coordinates', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='places.coordinates')),
                ('images', models.ManyToManyField(blank=True, to='places.Image')),
            ],
        ),
    ]
