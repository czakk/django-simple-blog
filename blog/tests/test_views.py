import blog.tests.testing_utils as testing_utils
import unittest

from blog.models import Post, Comment
from blog.forms import CommentForm, PostForm

from django.test import TestCase
from django.contrib.auth.models import User

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
        self.assertContains(response, f'Rating: {comment.rating}')

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

    @unittest.skip
    def test_success_message_after_add_comment(self):
        self.client.post(f'/{self.post.id}/{self.post.slug}/',
                                    data={'post': self.post,
                                          'author': 'Adam',
                                          'text': 'Test Comment',
                                          'rating': 2})
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        form = CommentForm()
        self.assertContains(response, 'Your comment has been added.')
        self.assertNotContains(response, form.as_p())

    @unittest.skip
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

    def test_display_only_active_comments(self):
        Comment.objects.create(post=self.post, author='John', text='Great post!')
        Comment.objects.create(post=self.post, author='John', text='Banned words', active=False)
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, 'Great post!')
        self.assertNotContains(response, 'Banned words')

    def test_there_is_no_avg_rating_if_no_ratings(self):
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, 'No ratings')
        self.assertNotContains(response, 'Average rating:')
    def test_post_avg_rating_on_detail_page(self):
        Comment.objects.create(post=self.post, rating=3)
        Comment.objects.create(post=self.post, rating=5)
        Comment.objects.create(post=self.post, rating=2)
        response = self.client.get(f'/{self.post.id}/{self.post.slug}/')
        self.assertContains(response, "Average rating: 3.33")


class TestPostAdd(TestCase):
    def setUp(self):
        self.user = testing_utils.create_user_john()

    def test_is_post_new_use_post_new_template(self):
        response = self.client.get('/new/')
        self.assertTemplateUsed(response, 'blog/post/new.html')

    @unittest.skip
    def test_post_new_page_display_new_post_form(self):
        response = self.client.get('/new/')
        form = PostForm()
        self.assertContains(response, form.as_p())

    def test_view_can_create_object_if_form_is_valid(self):
        self.assertEquals(Post.objects.count(), 0)
        self.client.post('/new/', data={'title': 'Test Title', 'text': 'Test'})
        self.assertEquals(Post.objects.count(), 1)

    def test_if_user_authenticated_then_author_will_be_user(self):
        self.client.force_login(self.user)
        self.client.post(self.client.post('/new/', data={'title': 'Test', 'text': 'Test'}))
        self.assertEquals(Post.objects.first().author, self.user)


    def test_if_anonymous_user_create_post_then_author_will_be_guest_user_model(self):
        self.client.post(self.client.post('/new/',
                                          data={'title': 'Test',
                                                'text': 'Test'}))
        guest = User.objects.get(username='Guest')
        self.assertEquals(Post.objects.first().author, guest)

    def test_if_guest_add_post_then_status_will_be_pending_and_dont_be_displayed(self):
        self.client.post(self.client.post('/new/',
                                          data={'title': 'Test',
                                                'text': 'Test'}))
        post = Post.objects.first()
        response = self.client.get(post.get_absolute_url())

        self.assertEquals(response.status_code, 404)

    def test_if_user_is_staff_post_instantly_published(self):
        staff_user = User.objects.create(username='Josh', is_staff=True)
        self.client.force_login(staff_user)
        self.client.post(self.client.post('/new/', data={'title': 'Test', 'text': 'test'}))
        self.assertEquals(Post.objects.first().status, 'published')

    def test_view_redirect_to_post_detail_after_adding_post_if_user_is_staff(self):
        staff_user = User.objects.create(username='Josh', is_staff=True)
        self.client.force_login(staff_user)
        response = self.client.post('/new/', data={'title': 'Test', 'text': 'test'})
        self.assertRedirects(response, Post.objects.first().get_absolute_url())



