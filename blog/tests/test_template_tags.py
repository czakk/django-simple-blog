import blog.tests.testing_utils as testing_utils

from blog.models import Post, Comment
from blog.templatetags import blog_tags as tags

from django.test import TestCase


class TestTags(TestCase):
    def test_get_post_avg_rating(self):
        post =  Post.objects.create(author=testing_utils.create_user_john(), title='Test')
        self.assertEquals(tags.get_post_avg_rating(post), 0)
        Comment.objects.create(post=post, author='Jack', rating=5)
        Comment.objects.create(post=post, author='Adam', rating=3)
        Comment.objects.create(post=post, author='Alex', rating=1)
        self.assertEquals(tags.get_post_avg_rating(post), 3.0)
        Comment.objects.create(post=post, author='Chris', rating=4)
        self.assertEquals(tags.get_post_avg_rating(post), 3.25)