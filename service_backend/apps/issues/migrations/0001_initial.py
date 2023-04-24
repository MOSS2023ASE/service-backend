# Generated by Django 3.2.18 on 2023-04-19 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chapters', '0001_initial'),
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=3071)),
                ('counsel_at', models.TimeField(null=True)),
                ('review_at', models.TimeField(null=True)),
                ('status', models.IntegerField()),
                ('anonymous', models.IntegerField()),
                ('score', models.IntegerField(null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='chapters.chapter')),
                ('counselor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counselor_issues', to='users.user')),
                ('reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_issues', to='users.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_issues', to='users.user')),
            ],
            options={
                'db_table': 'issues',
            },
        ),
        migrations.CreateModel(
            name='ReviewIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField()),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_issues', to='issues.issue')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_review_issues', to='users.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review_issues', to='users.user')),
            ],
            options={
                'db_table': 'review_issues',
            },
        ),
        migrations.CreateModel(
            name='LikeIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_issues', to='issues.issue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_issues', to='users.user')),
            ],
            options={
                'db_table': 'like_issues',
            },
        ),
        migrations.CreateModel(
            name='FollowIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_issues', to='issues.issue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_issues', to='users.user')),
            ],
            options={
                'db_table': 'follow_issues',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=3071)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='issues.issue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.user')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='AdoptIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField()),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adopt_issues', to='issues.issue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adopt_issues', to='users.user')),
            ],
            options={
                'db_table': 'adopt_issues',
            },
        ),
    ]
