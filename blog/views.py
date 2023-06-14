from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
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
    new_comment = None

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
                   'new_comment': new_comment})