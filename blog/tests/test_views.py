import blog.tests.testing_utils as testing_utils
import unittest

from blog.models import Post, Comment
from blog.forms import CommentForm

from django.test import TestCase


# Create your tests here.


class TestHomePage(TestCase):
    def setUp(self):
        self.user = testing_utils.create_user_john()
    def test_user_can_access_homepage(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_post_list_on_homepage(self):
        testing_utils.create_posts(3, self.user)
        response = self.client.get('')
        self.assertContains(response, 'Test 1')
        self.assertContains(response, 'Test 2')
        self.assertContains(response, 'Test 3')

    def test_is_homepage_using_home_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'blog/post/home.html')

    def test_pagination_on_homepage(self):
        # homepage should display only 5 posts per page
        testing_utils.create_posts(8, self.user)
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

    def test_homepage_displays_only_published_posts(self):
        Post.objects.create(title='Published post', author=self.user, status='published')
        Post.objects.create(title='Pending post', author=self.user)
        response = self.client.get('')
        self.assertContains(response, 'Published post')
        self.assertNotContains(response, 'Pending pos')

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

    def test_comment_display_on_post_detail(self):
        comment = Comment.objects.create(post=self.post, author='Jack', text='Good post', rating=4)
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, f'Created {comment.created.strftime("%d-%m-%Y %H:%M")} by {comment.author}')
        self.assertContains(response, comment.text)

    def test_comments_display_on_post_detail(self):
        Comment.objects.create(post=self.post, author='Jack', text='Good post', rating=4)
        Comment.objects.create(post=self.post, author='Adam', text='Nice!', rating=5)
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, 'Good post')
        self.assertContains(response, 'Nice!')

    def test_display_information_about_no_comments(self):
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, 'There are no comment\'s yet.')

    def test_post_method_to_post_detail_creating_object(self):
        self.assertEquals(Comment.objects.count(), 0)
        self.client.post(f'/{self.post.id}/{self.post.slug}/',
                         data={'post': self.post,
                               'author': 'John',
                               'text': 'Test',
                               'rating': 2})
        self.assertEquals(Comment.objects.count(), 1)

    def test_information_about_added_comment(self):
        self.client.post(f'/{self.post.id}/{self.post.slug}/',
                                    data={'post': self.post,
                                          'author': 'Adam',
                                          'text': 'Test Comment',
                                          'rating': 2})
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        form = CommentForm()
        self.assertContains(response, 'Your comment has been added.')
        self.assertNotContains(response, form.as_p())

    def test_user_get_comment_form_if_not_new_comment(self):
        form = CommentForm()
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, form.as_p())
        self.assertNotContains(response, 'Your comment has been added.')


    def test_redirect_to_post_detail_after_comment(self):
        response = self.client.post(f'/{self.post.id}/{self.post.slug}/',
                                    data={'post': self.post,
                                          'author': 'Adam',
                                          'text': 'Test Comment',
                                          'rating': 2})
        self.assertRedirects(response, self.post.get_absolute_url())