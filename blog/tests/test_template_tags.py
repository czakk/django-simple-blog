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

    def test_get_the_best_rated_posts(self):
        user = testing_utils.create_user_john()
        most_rated = Post.objects.create(author=user, title='1')
        last_rated = Post.objects.create(author=user, title='3')
        second_rated = Post.objects.create(author=user, title='2')
        additional = Post.objects.create(author=user, title='4')
        Comment.objects.create(post=most_rated, rating=5)
        Comment.objects.create(post=second_rated, rating=4)
        Comment.objects.create(post=last_rated, rating=3)
        Comment.objects.create(post=additional, rating=1)

        ranking = tags.get_the_best_rated_posts(count=3)
        self.assertEquals(ranking[0], most_rated)
        self.assertEquals(ranking[1], second_rated)
        self.assertEquals(ranking[2], last_rated)
        with self.assertRaises(IndexError):
            print(ranking[3])