# Generated by Django 4.2.1 on 2023-05-31 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_guess_approved_guess_downvotes_guess_upvotes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guess',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guesses', to='main.sample'),
        ),
    ]
