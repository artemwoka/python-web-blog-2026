from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    post_list = Post.published.all()
    # Посторінкове розбиття на 2 пости на сторінку
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page_number)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request, 'blog/post/detail.html', {'post': post})