import uuid

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class PostCustomUser(AbstractUser):
    country = models.CharField(max_length=100, null=True, blank=True)
    city_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=1000, help_text='User biography', blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='user_profile_images/')


class Post(models.Model):
    CATEGORY_CHOICES = (
        ("Programming", "Programming"),
        ("Health", "Health"),
        ("Fashion", "Fashion"),
        ("Food", "Food"),
        ("Travel", "Travel"),
        ("Business", "Business"),
        ("Art", "Art"),
        ("Other", "Other"),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=None)
    title = models.CharField(max_length=50)
    creat_date = models.DateField(auto_now_add=True)
    body = models.TextField(help_text='Post body')
    author = models.ForeignKey(PostCustomUser, on_delete=models.PROTECT,  db_constraint=False)
    description = models.TextField(max_length=800, help_text='Post description, max 1500 symbols', default=None)
    posted = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to='user_post_images/')
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True, default=uuid.uuid1)

    class Meta:
        ordering = ['-posted', '-creat_date']

    def __str__(self):
        return f'{self.title}'

    def save(self, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(**kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment_body = models.TextField()
    user = models.ForeignKey(
        PostCustomUser,
        null=True, blank=True, related_name='comment_user', on_delete=models.SET_NULL, db_constraint=False)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
