from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post


def homepage(request):
    posts = Post.objects.all()

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
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})