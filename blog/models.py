from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_comments.moderation import CommentModerator
from django_comments_xtd.moderation import moderator

class PostCommentModerator(CommentModerator):
    email_notification = True
    auto_moderate_field = 'publish'
    moderate_after = 365


class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset()\
                                         .filter(publish__lte=timezone.now())


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    objects = PublicManager()  # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       kwargs={'year': self.publish.year,
                               'month': self.publish.strftime('%b'),
                               'day': self.publish.strftime('%d'),
                               'slug': self.slug})


moderator.register(Post, PostCommentModerator)