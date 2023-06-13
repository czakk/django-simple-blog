from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9,
                              choices=STATUS_CHOICES,
                              default='pending')

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id,
                                                 self.slug])