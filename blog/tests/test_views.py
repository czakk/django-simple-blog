import blog.tests.testing_utils as testing_utils
import unittest

from django.contrib.auth.models import User
from blog.models import Post
from django.test import TestCase


# Create your tests here.


class TestHomePage(TestCase):
    def test_user_can_access_homepage(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_post_list_on_homepage(self):
        user = testing_utils.create_user_john()
        testing_utils.create_posts(3, user)
        response = self.client.get('')
        self.assertContains(response, 'Test 1')
        self.assertContains(response, 'Test 2')
        self.assertContains(response, 'Test 3')

    def test_is_homepage_using_home_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'blog/post/home.html')

    def test_pagination_on_homepage(self):
        # homepage should display only 5 posts per page
        testing_utils.create_posts(8, testing_utils.create_user_john())
        response = self.client.get('')
        for i in range(1, 4):
            self.assertNotContains(response, f'Test {i}')
        for i in range(4, 9):
            self.assertContains(response, f'Test {i}')

        response = self.client.get('', {'page': 2})

        for i in range(1, 4):
            self.assertContains(response, f'Test {i}')
        for i in range(4, 9):
            self.assertNotContains(response, f'Test {i}')

class TestPostDetail(TestCase):
    def setUp(self):
        self.user = testing_utils.create_user_john()
        self.post = Post.objects.create(title='Test 1', author=self.user, status='published')

    def test_is_created_post_is_published(self):
        self.assertEquals(self.post, Post.objects.first())

    def test_can_get_detail_page(self):
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertEquals(response.status_code, 200)

    def test_detail_page_return_404_when_post_is_pending(self):
        pending_post = Post.objects.create(title='Test Pending Post', author=self.user)
        response = self.client.get(f'/{pending_post.id}/{pending_post.slug}/')
        self.assertEquals(response.status_code, 404)
    def test_detail_page_contains_post(self):
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.created.strftime('%d-%m-%Y %H:%M'))
        self.assertContains(response, self.post.text)

    def test_is_detail_page_using_post_detail_template(self):
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertTemplateUsed(response, 'blog/post/detail.html')
