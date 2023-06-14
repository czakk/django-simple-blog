import blog.tests.testing_utils as testing_utils

from django.test import TestCase

from blog.forms import CommentForm
from blog.models import Post, Comment


class TestCommentForm(TestCase):
    def test_is_form_validation_assert_false_when_empty_field(self):
        post = Post.objects.create(title='Test', author=testing_utils.create_user_john())
        comment = CommentForm(data={'post': post, 'author': '', 'text': 'Good', 'rating': 5})

        self.assertFalse(comment.is_valid())

    def test_is_form_validation_assert_true(self):
        post = Post.objects.create(title='Test', author=testing_utils.create_user_john())
        comment = CommentForm(data={'post': post, 'author': 'Adam', 'text': 'Good', 'rating': 5})

        self.assertTrue(comment.is_valid())