# Generated by Django 3.2.18 on 2023-04-11 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subjects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='subjects.subject')),
            ],
            options={
                'db_table': 'chapters',
            },
        ),
    ]