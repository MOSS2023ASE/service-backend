# Generated by Django 3.2.18 on 2023-04-11 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('password_digest', models.CharField(max_length=255)),
                ('mail', models.EmailField(max_length=254)),
                ('avatar', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
