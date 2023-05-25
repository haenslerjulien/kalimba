# Generated by Django 4.2.1 on 2023-05-25 14:27

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', django_mysql.models.SizedTextField(blank=True, null=True, size_class=1)),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', django_mysql.models.SizedTextField(blank=True, null=True, size_class=1)),
            ],
        ),
    ]