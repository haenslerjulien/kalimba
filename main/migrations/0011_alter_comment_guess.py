# Generated by Django 4.2.1 on 2023-06-01 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_guess_sample'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='guess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.guess'),
        ),
    ]
