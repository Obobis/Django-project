from audioop import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default = 'draft')

    tags = TaggableManager()

    def get_absolute_url(self):
        return f"/posts/{self.publish.year}/{self.publish.month:02}/{self.publish.day:02}/{self.slug}/"
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Reply(models.Model):
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Reply by {} on {}'.format(self.name, self.post)

'''class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    body = RichTextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default = 'draft')

    tags = TaggableManager()

    def get_absolute_url(self):
        return f"/articles/{self.publish.year}/{self.publish.month:02}/{self.publish.day:02}/{self.slug}/"
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title'''