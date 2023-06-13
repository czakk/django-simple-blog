import blog.tests.testing_utils as testing_utils
import unittest

from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post


class TestPost(TestCase):
    def setUp(self):
        self.user = testing_utils.create_user_john()

    def test_title_as_default_text(self):
        post = Post()
        post.title = 'Test Title'
        post.author = self.user
        post.save()
        self.assertEquals(str(post), 'Test Title')

    def test_model_get_slug_from_title_when_not_provide(self):
        post = Post()
        post.title = 'Test Title'
        post.author = self.user
        post.save()
        self.assertEquals(post.slug, 'test-title')

    def test_get_absolute_url(self):
        post = Post.objects.create(title='Test Title', author=self.user)
        self.assertEquals(post.get_absolute_url(), '/1/test-title/')

