from django import template
from django.db.models import Avg

from ..models import Post


register = template.Library()


@register.simple_tag
def get_post_avg_rating(post: Post):
    average_rating = post.comments.aggregate(avg=Avg('rating'))['avg']
    return average_rating if average_rating else 0

#TODO most rated post list