# Generated by Django 3.2.18 on 2023-04-11 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewissues',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]