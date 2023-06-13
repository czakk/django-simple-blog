from django.contrib.auth.models import User
from blog.models import Post

def create_posts(amount, author):
    for i in range(1, amount + 1):
        Post.objects.create(title=f'Test {i}', author=author)

def create_user_john():
    return User.objects.create(username='john',
                               email='example.com',
                               password='123')