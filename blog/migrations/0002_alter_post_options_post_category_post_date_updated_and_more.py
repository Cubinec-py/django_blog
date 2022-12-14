# Generated by Django 4.0.7 on 2022-08-28 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-posted', '-creat_date']},
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Programming', 'Programming'), ('Health', 'Health'), ('Fashion', 'Fashion'), ('Food', 'Food'), ('Travel', 'Travel'), ('Business', 'Business'), ('Art', 'Art'), ('Other', 'Other')], default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(default=None, help_text='Post description, max 1500 symbols', max_length=800),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_post_images/'),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=uuid.uuid1, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(help_text='Post body'),
        ),
        migrations.AlterField(
            model_name='postcustomuser',
            name='city_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='postcustomuser',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='postcustomuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile_images/'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('comment_body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
