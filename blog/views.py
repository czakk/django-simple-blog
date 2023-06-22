from django.contrib import messages
from django.contrib.auth.models import AnonymousUser, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm, PostForm
from .models import Post


def homepage(request):
    posts = Post.objects.all().filter(status='published')

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request,
                  'blog/post/home.html',
                  {'posts': posts})

def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug, status='published')
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect(post)
    else:
        form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'form': form,
                   'comments': comments})

def post_add(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)

            if isinstance(request.user, User):
                user = request.user
            else:
                user = User.objects.get_or_create(username='Guest')[0]
                # try:
                #     new_post.author = User.objects.get(username='Guest')
                # except User.DoesNotExist:
                #     new_post.author = User.objects.create(username='Guest')

            new_post.author = user

            messages.success(request, 'Your post has been added!')

            if new_post.author.is_staff:
                new_post.status = 'published'
                new_post.save()
                return redirect(new_post)

            new_post.save()
            messages.info(request, 'Your post is pending and waiting on staff acceptation.')

            return redirect('blog:homepage')
    else:
        form = PostForm()
    return render(request,
                  'blog/post/new.html',
                  {'form': form})