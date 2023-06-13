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
        self.assertNotContains(response, 'Test 1')
        self.assertNotContains(response, 'Test 2')
        self.assertNotContains(response, 'Test 3')
        self.assertContains(response, 'Test 4')
        self.assertContains(response, 'Test 5')
        self.assertContains(response, 'Test 6')
        self.assertContains(response, 'Test 7')
        self.assertContains(response, 'Test 8')
        response = self.client.get('', {'page': 2})
        self.assertContains(response, 'Test 1')
        self.assertContains(response, 'Test 2')
        self.assertContains(response, 'Test 3')
        self.assertNotContains(response, 'Test 4')
        self.assertNotContains(response, 'Test 5')
        self.assertNotContains(response, 'Test 6')
        self.assertNotContains(response, 'Test 7')
        self.assertNotContains(response, 'Test 8')