# Generated by Django 4.2.1 on 2023-05-30 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_sample_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sample',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='sample',
            name='file',
            field=models.FileField(blank=True, default='', upload_to='samples/'),
        ),
    ]