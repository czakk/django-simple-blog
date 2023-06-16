from django import template
from django.db.models import Avg

from ..models import Post


register = template.Library()


@register.simple_tag
def get_post_avg_rating(post: Post):
    average_rating = post.comments.aggregate(avg=Avg('rating')).get('avg', 0)
    return average_rating if average_rating else 0

@register.simple_tag
def get_the_best_rated_posts(count=5):
    posts = filter(lambda post: get_post_avg_rating(post) > 0, Post.objects.all())
    return sorted(posts, key=get_post_avg_rating, reverse=True)[:count]
