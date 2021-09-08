from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager,
                     self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # makes it SEO (search-engine-optimization) friendly URLs
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # this defines a many-to-one relationship
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # saves date once it's created
    created = models.DateTimeField(auto_now_add=True)
    # saves date everytime you save
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()  # The default manager
    published = PublishManager()  # our custom manager

    # canonical
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    # sorting in descending by using the - sign
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

