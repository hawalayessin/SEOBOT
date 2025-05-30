# Generated by Django 4.2.14 on 2024-07-22 11:55

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryTitle', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('dateLastUpdate', models.DateField(auto_now=True)),
                ('idCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SEORobotapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='SEOMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_key', models.CharField(max_length=255)),
                ('meta_value', models.CharField(max_length=255)),
                ('idPage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SEORobotapp.page')),
            ],
        ),
    ]
