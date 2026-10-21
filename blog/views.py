from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    """Альтернативне в'ю списку постів"""

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


    
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

def post_share(request, post_id):
    # Отримати пост за його id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма була відправлена на обробку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля форми успішно пройшли валідацію
            cd = form.cleaned_data
            # відправити електронний лист
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} рекомендує вам прочитати '{post.title}'"
            message = f"Прочитайте '{post.title}' за посиланням ({post_url})\n\n"\
                        f"{cd['name']} коментарі: {cd['comments']}"
            send_mail(subject, message, 'blog@fake.mail', [cd['to']])
            sent= True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})